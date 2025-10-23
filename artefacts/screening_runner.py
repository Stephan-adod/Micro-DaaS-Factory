#!/usr/bin/env python3
import os
import sys
import json
import glob
from datetime import datetime, timezone, timedelta

try:
    import jsonschema
except Exception:
    jsonschema = None

SCHEMA_VERSION = "v3.1-refine-1"


def emit(level, **fields):
    payload = {"level": level}
    payload.update(fields)
    print(json.dumps(payload))


def iso_to_dt(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def now_utc(arg_now=None):
    if arg_now:
        return iso_to_dt(arg_now)
    env = os.getenv("NOW_UTC", "").strip()
    if env:
        return iso_to_dt(env)
    return datetime.now(timezone.utc)


def _parse_scalar(value):
    if value == "":
        return ""
    if value.startswith("\"") and value.endswith("\""):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "~"}:
        return None
    try:
        if "." in value or "e" in value.lower():
            return float(value)
        return int(value)
    except ValueError:
        return value


def _simple_yaml_parse(text):
    root = {}
    stack = [(-1, root)]
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        line = line.strip()
        if ":" not in line:
            raise ValueError(f"Unsupported YAML line: {raw}")
        key, rest = line.split(":", 1)
        key = key.strip()
        rest = rest.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if rest == "":
            value = {}
            parent[key] = value
            stack.append((indent, value))
        else:
            parent[key] = _parse_scalar(rest)
    return root


def load_config():
    path = "configs/telemetry/config.yaml"
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    try:
        import yaml  # type: ignore
    except Exception:
        return _simple_yaml_parse(text)
    return yaml.safe_load(text)


def compute_health(e, w):
    mROI = float(e["mROI"])
    uplift = float(e["Uplift"])
    delta_mape = float(e.get("delta_mape", e.get("ΔMAPE", 0.0)))
    freshness = float(e.get("Freshness", 0.0))
    return (
        w["mROI"] * mROI
        + w["uplift"] * uplift
        + w["delta_mape"] * (1 - delta_mape)
        + w["freshness"] * freshness
    )


def in_01(x):
    try:
        xf = float(x)
    except Exception:
        return False
    return 0.0 <= xf <= 1.0


def validate_bounds(e):
    keys = [("mROI", "mROI"), ("Uplift", "Uplift"), ("Freshness", "Freshness")]
    if "delta_mape" in e:
        keys.append(("delta_mape", "delta_mape"))
    elif "ΔMAPE" in e:
        keys.append(("ΔMAPE", "ΔMAPE"))
    for k, _ in keys:
        if not in_01(e.get(k)):
            raise ValueError(f"out_of_bounds:{k}:{e.get(k)}")


def schema_validate(payload):
    if jsonschema is None:
        emit("warn", code="jsonschema_missing", msg="jsonschema not installed; skipping strict validation")
        return
    with open("artefacts/governance_health_index.schema.json", "r", encoding="utf-8") as f:
        schema = json.load(f)
    jsonschema.validate(instance=payload, schema=schema)


def parse_args(argv):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write filled entries to _filled/")
    parser.add_argument(
        "--strict-window", action="store_true", help="fail if >threshold of entries are stale"
    )
    parser.add_argument("--now", type=str, default=None, help="override NOW_UTC (ISO8601)")
    return parser.parse_args(argv)


def main():
    args = parse_args(sys.argv[1:])
    cfg = load_config()
    now = now_utc(args.now)
    files = sorted(glob.glob("artefacts/health_records/*.json"))
    if not files:
        emit("error", code="no_files", msg="No health record files found.")
        return 2

    weights = cfg["weights"]
    tolerance = float(cfg["validation"]["tolerance"])
    window_days = int(cfg["validation"]["review_window_days"])
    strict_threshold = float(cfg["validation"]["strict_window_threshold"])
    weighted = bool(cfg["aggregation"]["weighted"])
    weight_field = cfg["aggregation"]["weight_field"]

    any_error = False
    aggregate = []

    for fp in files:
        with open(fp, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        if data.get("version") != SCHEMA_VERSION:
            emit(
                "warn",
                code="schema_version_mismatch",
                file=fp,
                version=data.get("version"),
                expected=SCHEMA_VERSION,
            )
        try:
            schema_validate(data)
        except Exception as exc:
            emit("error", code="schema_validation_failed", file=fp, msg=str(exc))
            any_error = True
            continue

        entries = data.get("entries", [])
        stale = 0
        filled = {
            "version": data.get("version"),
            "health_formula": data.get("health_formula"),
            "review_window_days": data.get("review_window_days"),
            "entries": [],
        }

        for entry in entries:
            try:
                validate_bounds(entry)
            except Exception as exc:
                emit("error", code="bounds", service=entry.get("service"), msg=str(exc))
                any_error = True
                continue

            ts = iso_to_dt(entry["timestamp"])
            if ts < (now - timedelta(days=window_days)):
                stale += 1
                emit("warn", code="stale_entry", service=entry.get("service"), timestamp=entry["timestamp"])

            calculated = compute_health(entry, weights)
            current = float(entry.get("Health", 0.0))
            if abs(current - calculated) > tolerance and args.write and current == 0.0:
                entry["Health"] = round(calculated, 6)
            entry_health = float(entry.get("Health", calculated))
            aggregate.append((entry, entry_health, entry.get(weight_field, 1.0)))
            filled["entries"].append(entry)

        if args.write:
            out_dir = "artefacts/health_records/_filled"
            os.makedirs(out_dir, exist_ok=True)
            out_fp = os.path.join(out_dir, os.path.basename(fp))
            with open(out_fp, "w", encoding="utf-8") as handle:
                json.dump(filled, handle, ensure_ascii=False, indent=2)

        ratio_stale = (stale / len(entries)) if entries else 0.0
        if args.strict_window and ratio_stale > strict_threshold:
            emit("error", code="stale_ratio", file=fp, ratio=ratio_stale)
            any_error = True

    if aggregate:
        if weighted:
            numerator = sum(health * weight for _, health, weight in aggregate)
            denominator = sum(weight for *_, weight in aggregate) or 1.0
            avg = numerator / denominator
        else:
            avg = sum(health for _, health, _ in aggregate) / len(aggregate)

        emit("info", code="avg_health", value=round(avg, 6))
        soft = float(cfg["validation"]["min_avg_health_soft"])
        hard = float(cfg["validation"]["min_avg_health_hard"])

        if avg < hard:
            emit("error", code="avg_below_hard", hard=hard, avg=avg)
            any_error = True
        elif avg < soft:
            emit("warn", code="avg_below_soft", soft=soft, avg=avg)

    return 1 if any_error else 0


if __name__ == "__main__":
    sys.exit(main())
