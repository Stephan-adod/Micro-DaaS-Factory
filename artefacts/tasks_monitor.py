#!/usr/bin/env python3
import argparse
import importlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
  import jsonschema
except Exception:
  jsonschema = None

if jsonschema is None:
  try:
    sys.path.append(str(Path(__file__).resolve().parent.parent))
    jsonschema = importlib.import_module("jsonschema")
  except Exception:
    jsonschema = None

SCHEMA_PATH = "artefacts/task_schema.json"
INDEX_PATH = "artefacts/tasks_index.json"

def iso(s):
  return datetime.fromisoformat(s.replace("Z", "+00:00"))

def now_utc(override=None):
  if override:
    return iso(override)
  env = os.getenv("NOW_UTC", "").strip()
  return iso(env) if env else datetime.now(timezone.utc)

def load_json(p):
  with open(p, "r", encoding="utf-8") as f:
    return json.load(f)

def validate_schema(index):
  if jsonschema is None or not hasattr(jsonschema, "validate"):
    print('[WARN] jsonschema not installed, skipping schema validation.')
    return True
  schema = load_json(SCHEMA_PATH)
  jsonschema.validate(instance=index, schema=schema)
  return True

def duplicate_ids(tasks):
  seen = set()
  dups = set()
  for t in tasks:
    ident = t.get("id")
    if ident in seen:
      dups.add(ident)
    seen.add(ident)
  return sorted(dups)

def unmet_dependencies(task, status_by_id):
  deps = task.get("depends_on") or []
  return [dep for dep in deps if status_by_id.get(dep) not in ("done", "skipped")]

def evaluate(index, ref_now):
  tasks = index.get("tasks", [])
  dups = duplicate_ids(tasks)
  status_by_id = {t.get("id"): t.get("status") for t in tasks}
  open_blocking = []
  warnings = []
  dep_errors = []
  evidence_errors = []
  for t in tasks:
    status = t.get("status")
    blocking = bool(t.get("blocking", True))
    due = t.get("due")
    next_due = t.get("next_due")
    t_due = iso(next_due or due) if (next_due or due) else None

    missing = unmet_dependencies(t, status_by_id)
    if missing:
      dep_errors.append({"id": t.get("id"), "title": t.get("title"), "missing": missing})

    if t.get("evidence_required") and status == "done" and not t.get("evidence"):
      evidence_errors.append({"id": t.get("id"), "title": t.get("title")})

    if status in ("done", "skipped"):
      continue

    if blocking:
      if t_due and ref_now > t_due:
        open_blocking.append((t["id"], t["title"], "overdue", t_due.isoformat()))
      elif status in ("open", "in_progress"):
        open_blocking.append((t["id"], t["title"], "open", t_due.isoformat() if t_due else None))
    else:
      if t_due and ref_now > t_due:
        warnings.append((t["id"], t["title"], "nonblocking_overdue", t_due.isoformat()))

  return open_blocking, warnings, dups, dep_errors, evidence_errors

def print_summary(open_blocking, warnings, dups, dep_errors, evidence_errors):
  def row(code, rec):
    return {
      "level": "error" if code.startswith("open") else "warn",
      "code": code,
      "id": rec[0],
      "title": rec[1],
      "due": rec[3],
    }

  logs = []
  for ident in dups:
    logs.append({"level": "error", "code": "duplicate_id", "id": ident})
  for dep in dep_errors:
    logs.append({"level": "error", "code": "unmet_dependencies", "id": dep["id"], "missing": dep["missing"]})
  for evidence in evidence_errors:
    logs.append({"level": "error", "code": "evidence_missing", "id": evidence["id"], "title": evidence["title"]})
  for r in open_blocking:
    logs.append(row("open_or_overdue_blocking", r))
  for w in warnings:
    logs.append(row("overdue_nonblocking", w))
  for l in logs:
    print(json.dumps(l))
  print(json.dumps({"level": "info", "code": "open_blocking_count", "value": len(open_blocking)}))
  print(json.dumps({"level": "info", "code": "dup_count", "value": len(dups)}))
  print(json.dumps({"level": "info", "code": "dep_error_count", "value": len(dep_errors)}))
  print(json.dumps({"level": "info", "code": "evidence_error_count", "value": len(evidence_errors)}))
  return len(open_blocking) + len(dups) + len(dep_errors) + len(evidence_errors)

def parse_args(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument("--now", type=str, default=None, help="override NOW_UTC (ISO8601)")
  parser.add_argument("--complete", type=str, default=None, help="mark task id as done (no writeback; policy-only)")
  parser.add_argument("--snooze", type=str, default=None, help="task id to snooze (no writeback; policy-only)")
  return parser.parse_args(argv)

def main():
  args = parse_args(sys.argv[1:])
  ref_now = now_utc(args.now)
  try:
    index = load_json(INDEX_PATH)
    validate_schema(index)
    open_blocking, warnings, dups, dep_errors, evidence_errors = evaluate(index, ref_now)
    hard_errors = print_summary(open_blocking, warnings, dups, dep_errors, evidence_errors)
    if hard_errors > 0:
      return 1
    return 0
  except Exception as ex:
    print(json.dumps({"level": "error", "code": "tasks_monitor_exception", "msg": str(ex)}))
    return 2

if __name__ == "__main__":
  sys.exit(main())
