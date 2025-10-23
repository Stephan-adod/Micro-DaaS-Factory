#!/usr/bin/env python3
import os, sys, json, glob, math
from datetime import datetime, timezone, timedelta

try:
    import jsonschema
except Exception:
    jsonschema = None

SCHEMA_VERSION = "v3.1-refine-1"

def iso_to_dt(s):
    return datetime.fromisoformat(s.replace("Z","+00:00"))

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
    with open("configs/telemetry/config.yaml","r",encoding="utf-8") as f:
        text = f.read()
    try:
        import yaml
    except Exception:
        return _simple_yaml_parse(text)
    return yaml.safe_load(text)

def compute_health(e, w):
    mROI = float(e["mROI"])
    Up = float(e["Uplift"])
    dM = float(e.get("delta_mape", e.get("ΔMAPE", 0.0)))
    Fr = float(e.get("Freshness", 0.0))
    return w["mROI"]*mROI + w["uplift"]*Up + w["delta_mape"]*(1 - dM) + w["freshness"]*Fr

def in_01(x):
    try:
        xf = float(x)
    except Exception:
        return False
    return 0.0 <= xf <= 1.0

def validate_bounds(e):
    keys = [("mROI","mROI"),("Uplift","Uplift"),("Freshness","Freshness")]
    if "delta_mape" in e: keys.append(("delta_mape","delta_mape"))
    elif "ΔMAPE" in e: keys.append(("ΔMAPE","ΔMAPE"))
    for k,_ in keys:
        if not in_01(e.get(k)):
            raise ValueError(f"out_of_bounds:{k}:{e.get(k)}")

def schema_validate(payload):
    if jsonschema is None:
        print('[WARN] jsonschema not installed, skipping strict schema validation.')
        return
    with open("artefacts/governance_health_index.schema.json","r",encoding="utf-8") as f:
        schema = json.load(f)
    jsonschema.validate(instance=payload, schema=schema)

def parse_args(argv):
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--write", action="store_true", help="write filled entries to _filled/")
    p.add_argument("--strict-window", action="store_true", help="fail if >threshold of entries are stale")
    p.add_argument("--now", type=str, default=None, help="override NOW_UTC (ISO8601)")
    p.add_argument("--gate", choices=["soft","hard"], default="hard", help="threshold to enforce (soft warns, hard errors)")
    return p.parse_args(argv)

def main():
    args = parse_args(sys.argv[1:])
    cfg = load_config()
    NOW = now_utc(args.now)
    files = sorted(glob.glob("artefacts/health_records/*.json"))
    if not files:
        print(json.dumps({"level":"error","code":"no_files","msg":"No health record files found."}))
        return 2

    w = cfg["weights"]
    tol = float(cfg["validation"]["tolerance"])
    window_days = int(cfg["validation"]["review_window_days"])
    strict_thr = float(cfg["validation"]["strict_window_threshold"])
    weighted = bool(cfg["aggregation"]["weighted"])
    weight_field = cfg["aggregation"]["weight_field"]

    any_error = False
    agg = []

    for fp in files:
        with open(fp,"r",encoding="utf-8") as f:
            data = json.load(f)

        if data.get("version") != SCHEMA_VERSION:
            print(json.dumps({"level":"warn","code":"schema_version_mismatch","file":fp,"version":data.get("version")}))
        try:
            schema_validate(data)
        except Exception as ex:
            print(json.dumps({"level":"error","code":"schema_validation_failed","file":fp,"msg":str(ex)}))
            any_error = True
            continue

        entries = data.get("entries", [])
        stale = 0
        filled = {"version": data.get("version"), "health_formula": data.get("health_formula"),
                  "review_window_days": data.get("review_window_days"), "entries": []}

        for e in entries:
            try:
                validate_bounds(e)
            except Exception as ex:
                print(json.dumps({"level":"error","code":"bounds","service":e.get("service"),"msg":str(ex)}))
                any_error = True
                continue

            ts = iso_to_dt(e["timestamp"])
            if ts < (NOW - timedelta(days=window_days)):
                stale += 1
                print(json.dumps({"level":"warn","code":"stale_entry","service":e.get("service"),"timestamp":e["timestamp"]}))

            calc = compute_health(e, w)
            current = float(e.get("Health", 0.0))

            # Abgleich & optionales Auto-Fill nur mit --write
            if abs(current - calc) > tol and args.write and current == 0.0:
                e["Health"] = round(calc, 6)

            # WICHTIG: In Dry-Run (kein --write) aggregieren wir calc statt 0.0-Platzhalter
            e_health = calc if current == 0.0 else current
            agg.append((e, e_health, e.get(weight_field, 1.0)))
            filled["entries"].append(e)

        if args.write:
            out_dir = "artefacts/health_records/_filled"
            os.makedirs(out_dir, exist_ok=True)
            out_fp = os.path.join(out_dir, os.path.basename(fp))
            with open(out_fp,"w",encoding="utf-8") as f:
                json.dump(filled, f, ensure_ascii=False, indent=2)

        ratio_stale = (stale/len(entries)) if entries else 0.0
        if args.strict_window and ratio_stale > strict_thr:
            print(json.dumps({"level":"error","code":"stale_ratio","file":fp,"ratio":ratio_stale}))
            any_error = True

    # Aggregation
    if agg:
        if weighted:
            num = sum(h*wgt for _,h,wgt in agg)
            den = sum(wgt for *_ , wgt in agg) or 1.0
            avg = num/den
        else:
            avg = sum(h for _,h,_ in agg)/len(agg)

        avg = round(avg, 6)
        print(json.dumps({"level":"info","code":"avg_health","value":avg}))
        soft = float(cfg["validation"]["min_avg_health_soft"])
        hard = float(cfg["validation"]["min_avg_health_hard"])

        if args.gate == "hard" and avg < hard:
            print(json.dumps({"level":"error","code":"avg_below_hard","hard":hard,"avg":avg}))
            any_error = True
        elif avg < soft:
            print(json.dumps({"level":"warn","code":"avg_below_soft","soft":soft,"avg":avg}))

    return 1 if any_error else 0

if __name__ == "__main__":
    sys.exit(main())
