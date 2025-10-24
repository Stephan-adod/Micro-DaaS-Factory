#!/usr/bin/env python3
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

def now_utc():
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

def evaluate(index, ref_now):
  tasks = index.get("tasks", [])
  open_blocking = []
  warnings = []
  for t in tasks:
    status = t.get("status")
    blocking = bool(t.get("blocking", True))
    due = t.get("due")
    next_due = t.get("next_due")
    t_due = iso(next_due or due) if (next_due or due) else None

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

  return open_blocking, warnings

def print_summary(open_blocking, warnings):
  def row(code, rec):
    return {
      "level": "error" if code.startswith("open") else "warn",
      "code": code,
      "id": rec[0],
      "title": rec[1],
      "due": rec[3],
    }

  logs = []
  for r in open_blocking:
    logs.append(row("open_or_overdue_blocking", r))
  for w in warnings:
    logs.append(row("overdue_nonblocking", w))
  for l in logs:
    print(json.dumps(l))
  print(json.dumps({"level": "info", "code": "open_blocking_count", "value": len(open_blocking)}))
  return len(open_blocking)

def main():
  ref_now = now_utc()
  try:
    index = load_json(INDEX_PATH)
    validate_schema(index)
    open_blocking, warnings = evaluate(index, ref_now)
    count = print_summary(open_blocking, warnings)
    if count > 0:
      return 1
    return 0
  except Exception as ex:
    print(json.dumps({"level": "error", "code": "tasks_monitor_exception", "msg": str(ex)}))
    return 2

if __name__ == "__main__":
  sys.exit(main())
