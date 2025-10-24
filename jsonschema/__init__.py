"""Minimal jsonschema-compatible validator for local use.
This is not a full implementation of JSON Schema. It only performs the
checks required by the task index schema used in this repository.
"""
from datetime import datetime

class ValidationError(Exception):
    pass


def _require(condition, message):
    if not condition:
        raise ValidationError(message)


def _is_iso_datetime(value):
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except Exception:
        return False


def validate(instance, schema):
    if not isinstance(instance, dict):
        raise ValidationError("Task index must be an object")

    version = instance.get("version")
    _require(isinstance(version, str) and version == "v3.1", "version must be 'v3.1'")

    owner = instance.get("owner")
    _require(isinstance(owner, str) and owner, "owner must be a non-empty string")

    tasks = instance.get("tasks")
    _require(isinstance(tasks, list) and len(tasks) >= 1, "tasks must be a non-empty list")

    for idx, task in enumerate(tasks):
        _validate_task(task, idx)


def _validate_task(task, idx):
    _require(isinstance(task, dict), f"task[{idx}] must be an object")

    required = ["id", "title", "phase", "type", "status", "owner", "created_at", "blocking"]
    for field in required:
        _require(field in task, f"task[{idx}] missing required field '{field}'")

    _require(isinstance(task["id"], str), f"task[{idx}].id must be string")
    _require(len(task["title"]) >= 3, f"task[{idx}].title too short")

    _require(task["type"] in {"recurring", "one_time"}, f"task[{idx}].type invalid")
    _require(task["status"] in {"open", "in_progress", "done", "skipped"}, f"task[{idx}].status invalid")
    _require(isinstance(task["blocking"], bool), f"task[{idx}].blocking must be boolean")

    for field in ("created_at", "due", "last_run", "next_due"):
        if field in task and task[field] is not None:
            _require(isinstance(task[field], str) and _is_iso_datetime(task[field]),
                     f"task[{idx}].{field} must be ISO datetime string")

    if "interval_days" in task:
        _require(isinstance(task["interval_days"], int) and task["interval_days"] >= 1,
                 f"task[{idx}].interval_days must be integer >= 1")

    if "evidence" in task:
        _validate_str_list(task["evidence"], f"task[{idx}].evidence")

    if "tags" in task:
        _validate_str_list(task["tags"], f"task[{idx}].tags")


def _validate_str_list(value, label):
    _require(isinstance(value, list), f"{label} must be list")
    for entry in value:
        _require(isinstance(entry, str), f"{label} entries must be strings")
