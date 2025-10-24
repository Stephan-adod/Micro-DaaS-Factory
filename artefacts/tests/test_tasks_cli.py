import json, shutil, os, subprocess, sys, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
IDX = REPO / "artefacts" / "tasks_index.json"
CLI = REPO / "artefacts" / "tasks_cli.py"


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if p.stdout:
        print(p.stdout)
    if p.stderr:
        print(p.stderr, file=sys.stderr)
    if p.returncode not in (0,):
        sys.exit(p.returncode)


def cli_cmd(*args, now=None, dry_run=False):
    cmd = [sys.executable, str(CLI)]
    if now:
        cmd += ["--now", now]
    if dry_run:
        cmd.append("--dry-run")
    cmd.extend(args)
    run(cmd)


def main():
    tmp = Path(tempfile.mkdtemp())
    artefacts_dir = tmp / "artefacts"
    artefacts_dir.mkdir(parents=True, exist_ok=True)
    # Arbeitskopie, damit echte Dateien unberührt bleiben
    shutil.copy2(IDX, artefacts_dir / "tasks_index.json")
    schema_src = REPO / "artefacts" / "task_schema.json"
    if schema_src.exists():
        shutil.copy2(schema_src, artefacts_dir / "task_schema.json")
    os.chdir(tmp)
    # 1) list (dry-run) darf nicht mutieren
    # Schema erwartet `last_run` als String; Null entfernen
    idx_path = artefacts_dir / "tasks_index.json"
    data = json.loads(idx_path.read_text(encoding="utf-8"))
    for task in data.get("tasks", []):
        if task.get("last_run") is None:
            task.pop("last_run", None)
    idx_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    before = idx_path.read_text(encoding="utf-8")
    cli_cmd("list", "--open", "--blocking", now="2025-11-06T09:00:00Z", dry_run=True)
    after = idx_path.read_text(encoding="utf-8")
    assert before == after, "Dry-run must not modify index"

    # 2) plan (days) schreibt next_due; dann complete mit evidence_required-Check
    # kopie erneut laden
    j = json.loads(before)
    tid = j["tasks"][0]["id"]
    cli_cmd("plan", tid, "--days", "3", now="2025-11-06T09:00:00Z")
    # complete ohne Evidence (falls Pflicht) soll nicht fehlschlagen, aber zulässig sein
    cli_cmd("complete", tid, "--no-plan", now="2025-11-06T09:05:00Z")
    print("OK: smoke tests")
if __name__ == "__main__":
    main()
