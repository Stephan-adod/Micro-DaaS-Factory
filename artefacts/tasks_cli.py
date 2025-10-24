#!/usr/bin/env python3
"""Task CLI for Codex-Native Task Index (v3.1)
Commands:
  list [--open] [--blocking] [--overdue] [--json]
  show <ID>
  complete <ID> [--now ISO] [--evidence PATH...] [--no-plan]
  snooze <ID> (--days N | --until ISO)
  plan <ID> [--days N | --until ISO]    # set/override next_due
  reopen <ID>
  add-evidence <ID> PATH [PATH ...]
  set-status <ID> (open|in_progress|done|skipped)
Flags:
  --now ISO      Reference time (deterministic ops)
  --dry-run      Preview only (no writeback)
"""
import argparse, json, os, sys
from datetime import datetime, timedelta, timezone

INDEX_PATH = "artefacts/tasks_index.json"
SCHEMA_PATH = "artefacts/task_schema.json"

def iso_dt(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def dt_iso(dt: datetime) -> str:
    # always UTC Z
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

def now_utc(override: str | None) -> datetime:
    if override:
        return iso_dt(override)
    env = os.getenv("NOW_UTC", "").strip()
    return iso_dt(env) if env else datetime.now(timezone.utc)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def try_jsonschema_validate(index):
    try:
        import jsonschema
    except Exception:
        return
    schema = load_json(SCHEMA_PATH)
    jsonschema.validate(index, schema)

def compute_next_due(task, ref_now: datetime) -> datetime | None:
    """Compute next_due from interval_days or rrule, else return existing due/next_due."""
    # priority: already present next_due > ref_now
    if task.get("next_due"):
        try:
            nd = iso_dt(task["next_due"])
            if nd > ref_now:
                return nd
        except Exception:
            pass
    # RRULE support (requires dateutil)
    rrule = task.get("rrule")
    if rrule:
        try:
            from dateutil.rrule import rrulestr
            rule = rrulestr(rrule, dtstart=iso_dt(task.get("last_run") or task.get("created_at")))
            nxt = rule.after(ref_now, inc=False)
            if nxt:
                return nxt
        except Exception:
            pass
    # interval_days fallback
    days = task.get("interval_days")
    if isinstance(days, int) and days > 0:
        last = task.get("last_run")
        base = iso_dt(last) if last else ref_now
        return base + timedelta(days=days)
    # fallback to due
    if task.get("due"):
        try:
            return iso_dt(task["due"])
        except Exception:
            return None
    return None

def sort_tasks(tasks):
    def key(t):
        prio = {"P0": 0, "P1": 1, "P2": 2}.get(t.get("priority","P1"), 1)
        due = t.get("next_due") or t.get("due")
        dd = iso_dt(due) if due else datetime.max.replace(tzinfo=timezone.utc)
        return (prio, dd, t.get("id",""))
    return sorted(tasks, key=key)

def find_task(index, tid):
    for t in index["tasks"]:
        if t.get("id") == tid:
            return t
    raise SystemExit(f"[ERROR] Task {tid} not found.")

def list_cmd(index, args, ref):
    items = index["tasks"]
    out = []
    for t in items:
        status = t.get("status")
        if args.open and status == "done":
            continue
        if args.blocking and not t.get("blocking", True):
            continue
        if args.overdue:
            due = t.get("next_due") or t.get("due")
            if not due or ref <= iso_dt(due):
                continue
        out.append(t)
    out = sort_tasks(out)
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        for t in out:
            due = t.get("next_due") or t.get("due")
            print(f"{t.get('id'):>16}  [{t.get('status'):<11}]  {t.get('title')}  "
                  f"prio={t.get('priority','P1')} blocking={t.get('blocking',True)} "
                  f"due={due}")
    return 0

def complete_cmd(index, args, ref):
    t = find_task(index, args.id)
    t["status"] = "done"
    t["last_run"] = dt_iso(ref)
    if args.evidence:
        t.setdefault("evidence", [])
        for p in args.evidence:
            if p not in t["evidence"]:
                t["evidence"].append(p)
    if not args.no_plan:
        nd = compute_next_due(t, ref)
        if nd:
            t["next_due"] = dt_iso(nd)
    return 0

def snooze_cmd(index, args, ref):
    t = find_task(index, args.id)
    if args.days is None and args.until is None:
        raise SystemExit("[ERROR] Provide --days or --until")
    nd = iso_dt(args.until) if args.until else ref + timedelta(days=int(args.days))
    t["next_due"] = dt_iso(nd)
    if t.get("status") == "done":
        t["status"] = "open"
    return 0

def plan_cmd(index, args, ref):
    t = find_task(index, args.id)
    nd = None
    if args.days:
        nd = ref + timedelta(days=int(args.days))
    elif args.until:
        nd = iso_dt(args.until)
    else:
        nd = compute_next_due(t, ref)  # recompute from rules
    if nd:
        t["next_due"] = dt_iso(nd)
    return 0

def reopen_cmd(index, args, ref):
    t = find_task(index, args.id)
    t["status"] = "open"
    return 0

def add_evidence_cmd(index, args, ref):
    t = find_task(index, args.id)
    t.setdefault("evidence", [])
    for p in args.paths:
        if p not in t["evidence"]:
            t["evidence"].append(p)
    return 0

def set_status_cmd(index, args, ref):
    t = find_task(index, args.id)
    t["status"] = args.status
    return 0

def build_parser():
    p = argparse.ArgumentParser(description="Task CLI for Codex Task Index")
    p.add_argument("--now", default=None, help="override NOW_UTC (ISO8601)")
    p.add_argument("--dry-run", action="store_true", help="no writeback")
    sp = p.add_subparsers(dest="cmd", required=True)

    s = sp.add_parser("list")
    s.add_argument("--open", action="store_true")
    s.add_argument("--blocking", action="store_true")
    s.add_argument("--overdue", action="store_true")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=list_cmd)

    s = sp.add_parser("show"); s.add_argument("id")
    def show_cmd(index, args, ref):
        print(json.dumps(find_task(index, args.id), ensure_ascii=False, indent=2)); return 0
    s.set_defaults(func=show_cmd)

    s = sp.add_parser("complete"); s.add_argument("id")
    s.add_argument("--evidence", nargs="*", default=None)
    s.add_argument("--no-plan", action="store_true")
    s.set_defaults(func=complete_cmd)

    s = sp.add_parser("snooze"); s.add_argument("id")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--days", type=int)
    g.add_argument("--until")
    s.set_defaults(func=snooze_cmd)

    s = sp.add_parser("plan"); s.add_argument("id")
    g = s.add_mutually_exclusive_group(required=False)
    g.add_argument("--days", type=int)
    g.add_argument("--until")
    s.set_defaults(func=plan_cmd)

    s = sp.add_parser("reopen"); s.add_argument("id")
    s.set_defaults(func=reopen_cmd)

    s = sp.add_parser("add-evidence"); s.add_argument("id"); s.add_argument("paths", nargs="+")
    s.set_defaults(func=add_evidence_cmd)

    s = sp.add_parser("set-status"); s.add_argument("id"); s.add_argument("status", choices=["open","in_progress","done","skipped"])
    s.set_defaults(func=set_status_cmd)
    return p

def main(argv=None):
    args = build_parser().parse_args(argv)
    ref = now_utc(args.now)
    idx = load_json(INDEX_PATH)
    rc = args.func(idx, args, ref)
    # resort before write
    idx["tasks"] = sort_tasks(idx["tasks"])
    if not args.dry_run:
        try_jsonschema_validate(idx)
        save_json(INDEX_PATH, idx)
    else:
        print("[DRY-RUN] No writeback performed.", file=sys.stderr)
    return rc

if __name__ == "__main__":
    sys.exit(main())
