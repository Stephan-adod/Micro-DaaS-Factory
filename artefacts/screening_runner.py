"""Utilities for governance screening tasks.

This module provides a small toolbox that CI jobs can invoke to validate the
governance repository.  The original implementation only contained helpers for
CODEOWNERS lookups and Markdown discovery.  The screening command that the
product team now runs locally performs additional checks – it validates
frontmatter metadata, verifies dependency freshness and emits machine- and
human-readable reports.

Instead of keeping an ad-hoc Python one-liner around, we embed the behaviour in
this module so it can be unit-tested and shipped without external dependencies.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

OWNER_REQ = "stephan-adod"
VERSION_REQ = "v3.1"
REQUIRED_FIELDS = [
    "title",
    "version",
    "status",
    "phase",
    "owner",
    "updated",
    "review_due",
    "retention",
    "dependencies",
    "linked_docs",
    "layer",
    "policy_source",
    "policy_version",
]
REVIEW_WINDOW_DAYS = 90


def _normalize_handle(value: str | None) -> str | None:
    """Return the canonical representation of a CODEOWNERS handle."""

    if value is None:
        return None
    return value.lstrip("@")


def _parse_codeowners(codeowners_path: Path) -> Dict[str, List[str]]:
    """Parse the CODEOWNERS file into a mapping of pattern → owners."""

    rules: Dict[str, List[str]] = {}
    if not codeowners_path.exists():
        return rules

    for raw_line in codeowners_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        pattern, *owners = parts
        rules[pattern] = [_normalize_handle(owner) for owner in owners]

    return rules


def check_codeowners(
    base_path: Path | str = Path("."),
    required_owner: str = OWNER_REQ,
    patterns: Iterable[str] | None = None,
) -> Dict[str, object]:
    """Check whether required CODEOWNERS coverage exists for select patterns."""

    base = Path(base_path)
    codeowners_path = base / "CODEOWNERS"
    normalized_required_owner = _normalize_handle(required_owner)

    result: Dict[str, object] = {
        "path": str(codeowners_path),
        "rules": _parse_codeowners(codeowners_path),
        "issues": [],
    }

    if not codeowners_path.exists():
        result["issues"].append("CODEOWNERS_missing")
        return result

    monitored_patterns = list(patterns or ("meta/*", "artefacts/*"))
    rules = result["rules"]
    for pattern in monitored_patterns:
        owners = rules.get(pattern, [])
        normalized_owners = [_normalize_handle(owner) for owner in owners]
        if normalized_required_owner not in normalized_owners:
            result["issues"].append(f"CODEOWNERS_{pattern}_missing_or_wrong")

    return result


def collect_markdowns(base_path: Path | str) -> List[Path]:
    """Collect Markdown files while respecting the CI ignore whitelist."""

    base = Path(base_path)
    ign_env = os.getenv(
        "GOV_IGNORE_PATTERNS",
        "_fixtures/;artefacts/screening_report;/.github/pull_request_template",
    )
    ignore_patterns = [pattern.strip() for pattern in ign_env.split(";") if pattern.strip()]

    markdown_paths: List[Path] = []
    for path in base.rglob("*.md"):
        path_str = str(path)
        if any(ignore in path_str for ignore in ignore_patterns):
            continue
        markdown_paths.append(path)

    return markdown_paths


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _split_frontmatter(text: str) -> Tuple[List[str], str] | Tuple[None, None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, None

    frontmatter_lines: List[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        frontmatter_lines.append(line.rstrip("\r"))
    else:
        return None, None

    return frontmatter_lines, "\n".join(lines[len(frontmatter_lines) + 2 :])


def _parse_scalar(value: str) -> object:
    value = value.strip()
    if not value:
        return ""

    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]

    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"

    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    return value


def parse_frontmatter(path: Path) -> Tuple[Dict[str, object] | None, str | None]:
    """Parse YAML-like frontmatter without external dependencies."""

    text = _read_text(path)
    split = _split_frontmatter(text)
    if split == (None, None):
        return None, "no_frontmatter"

    fm_lines, _ = split
    data: Dict[str, object] = {}
    current_key: str | None = None

    for raw_line in fm_lines:
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        stripped = line.lstrip()
        if stripped.startswith("- ") and current_key is not None:
            item = stripped[2:]
            list_value = data.setdefault(current_key, [])
            if isinstance(list_value, list):
                list_value.append(_parse_scalar(item))
            else:
                data[current_key] = [list_value, _parse_scalar(item)]
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not value:
            data[key] = []
            current_key = key
            continue

        parsed_value = _parse_scalar(value)
        data[key] = parsed_value
        current_key = key if isinstance(parsed_value, list) else None

    return data, None


def _iso_to_date(value: object) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None


def _exists_rel(base: Path, relative: str) -> bool:
    candidate = (base / relative).resolve()
    try:
        candidate.relative_to(base.resolve())
    except ValueError:
        return False
    return candidate.exists()


@dataclass
class DocumentEvaluation:
    path: str
    ok: bool
    issues: List[str]
    notes: List[str]
    frontmatter: Dict[str, object] | None
    freshness_days: int | None
    stale: bool


def evaluate_doc(path: Path, base: Path) -> DocumentEvaluation:
    rel_path = path.relative_to(base)
    frontmatter, err = parse_frontmatter(path)
    issues: List[str] = []
    notes: List[str] = []

    if err or frontmatter is None:
        issues.append(err or "frontmatter_error")
        return DocumentEvaluation(
            path=str(rel_path),
            ok=False,
            issues=issues,
            notes=notes,
            frontmatter=None,
            freshness_days=None,
            stale=False,
        )

    missing_fields = [field for field in REQUIRED_FIELDS if field not in frontmatter]
    if missing_fields:
        issues.append(f"missing_fields:{missing_fields}")

    owner = frontmatter.get("owner")
    if owner != OWNER_REQ:
        issues.append(f"owner_invalid:{owner}")

    version = frontmatter.get("version")
    if version != VERSION_REQ:
        issues.append(f"version_invalid:{version}")

    updated_date = _iso_to_date(frontmatter.get("updated"))
    freshness_days = None
    if updated_date is None:
        issues.append("updated_invalid_or_missing")
    else:
        today = datetime.utcnow().date()
        if updated_date > today:
            issues.append("updated_in_future")
        freshness_days = (today - updated_date).days

    review_due = _iso_to_date(frontmatter.get("review_due"))
    if review_due is None:
        issues.append("review_due_invalid_or_missing")
    elif updated_date is not None and review_due > updated_date + timedelta(days=REVIEW_WINDOW_DAYS):
        issues.append("review_due_exceeds_90d")

    layer = frontmatter.get("layer")
    if not layer:
        issues.append("layer_missing")
    status = frontmatter.get("status")
    if not status:
        issues.append("status_missing")
    phase = frontmatter.get("phase")
    if not phase:
        issues.append("phase_missing")

    dependencies = frontmatter.get("dependencies") or []
    if isinstance(dependencies, str):
        dependencies = [dependencies]
    linked_docs = frontmatter.get("linked_docs") or []
    if isinstance(linked_docs, str):
        linked_docs = [linked_docs]

    missing_deps = [dep for dep in dependencies if not _exists_rel(base, dep)]
    if missing_deps:
        issues.append(f"missing_dependencies:{missing_deps}")

    missing_links = [doc for doc in linked_docs if not _exists_rel(base, doc)]
    if missing_links:
        issues.append(f"missing_linked_docs:{missing_links}")

    stale = False
    if updated_date is not None and dependencies:
        newer_deps = []
        for dep in dependencies:
            dep_path = base / dep
            if not dep_path.exists():
                continue
            dep_frontmatter, dep_err = parse_frontmatter(dep_path)
            if dep_err or not dep_frontmatter:
                continue
            dep_updated = _iso_to_date(dep_frontmatter.get("updated"))
            if dep_updated and dep_updated > updated_date:
                newer_deps.append({"dep": dep, "dep_updated": str(dep_updated)})
        if newer_deps:
            stale = True
            issues.append(f"stale_due_to_deps:{newer_deps}")

    frontmatter_snapshot = {
        "title": frontmatter.get("title"),
        "version": version,
        "status": status,
        "phase": phase,
        "owner": owner,
        "updated": str(updated_date) if updated_date else None,
        "review_due": str(review_due) if review_due else None,
        "retention": frontmatter.get("retention"),
        "dependencies": dependencies,
        "linked_docs": linked_docs,
        "layer": layer,
        "policy_source": frontmatter.get("policy_source"),
        "policy_version": frontmatter.get("policy_version"),
        "review_status": frontmatter.get("review_status"),
    }

    return DocumentEvaluation(
        path=str(rel_path),
        ok=not issues,
        issues=issues,
        notes=notes,
        frontmatter=frontmatter_snapshot,
        freshness_days=freshness_days,
        stale=stale,
    )


def run_screening(base_path: Path | str = Path(".")) -> Dict[str, object]:
    base = Path(base_path).resolve()
    markdowns = sorted({path.resolve() for path in collect_markdowns(base)})
    evaluations = [evaluate_doc(path, base) for path in markdowns]

    passed = [doc for doc in evaluations if doc.ok]
    failed = [doc for doc in evaluations if not doc.ok]
    stale_count = sum(1 for doc in evaluations if doc.stale)
    freshness_values = [doc.freshness_days for doc in evaluations if doc.freshness_days is not None]
    max_fresh = max(freshness_values) if freshness_values else None
    avg_fresh = (
        round(sum(freshness_values) / len(freshness_values), 1) if freshness_values else None
    )

    codeowners = check_codeowners(base)

    summary = {
        "scanned_files": len(evaluations),
        "passed": len(passed),
        "failed": len(failed),
        "stale": stale_count,
        "docs_freshness_max_days": max_fresh,
        "docs_freshness_avg_days": avg_fresh,
        "codeowners": codeowners,
        "timestamp_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "rules": {
            "required_fields": REQUIRED_FIELDS,
            "owner_required": OWNER_REQ,
            "version_required": VERSION_REQ,
            "review_due_window_days": REVIEW_WINDOW_DAYS,
        },
    }

    return {
        "summary": summary,
        "results": [doc.__dict__ for doc in evaluations],
    }


def write_reports(base_path: Path | str = Path(".")) -> Path:
    base = Path(base_path)
    artefacts_dir = base / "artefacts"
    artefacts_dir.mkdir(parents=True, exist_ok=True)

    report = run_screening(base)

    json_path = artefacts_dir / "screening_report.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    def _badge(ok: bool) -> str:
        return "✅" if ok else "❌"

    lines: List[str] = []
    summary = report["summary"]
    lines.append("# Repo Screening Report · v3.1\n")
    lines.append(f"- Timestamp (UTC): {summary['timestamp_utc']}")
    lines.append(
        f"- Files: {summary['scanned_files']} · Pass: {summary['passed']} · Fail: {summary['failed']} · Stale: {summary['stale']}"
    )
    if summary["docs_freshness_avg_days"] is not None:
        lines.append(
            f"- Docs Freshness: avg {summary['docs_freshness_avg_days']} d · max {summary['docs_freshness_max_days']} d\n"
        )
    lines.append("## CODEOWNERS\n")
    codeowners = summary["codeowners"]
    if codeowners.get("path"):
        lines.append(f"- Path: `{codeowners['path']}`")
        if codeowners.get("issues"):
            lines.append(f"- Issues: {codeowners['issues']}")
        else:
            lines.append("- Issues: none")
    else:
        lines.append("- ❌ CODEOWNERS file missing")
    lines.append("\n## Files\n")

    for doc in report["results"]:
        frontmatter = doc.get("frontmatter") or {}
        lines.append(f"### {_badge(doc['ok'])} `{doc['path']}`")
        lines.append(
            "- title: {title} · version: {version} · status: {status} · phase: {phase} · layer: {layer}".format(
                title=frontmatter.get("title"),
                version=frontmatter.get("version"),
                status=frontmatter.get("status"),
                phase=frontmatter.get("phase"),
                layer=frontmatter.get("layer"),
            )
        )
        lines.append(
            "- owner: {owner} · updated: {updated} · review_due: {review_due} · freshness_days: {freshness}".format(
                owner=frontmatter.get("owner"),
                updated=frontmatter.get("updated"),
                review_due=frontmatter.get("review_due"),
                freshness=doc.get("freshness_days"),
            )
        )
        if doc.get("stale"):
            lines.append("- **STALE**: deps newer than self")
        if doc.get("issues"):
            lines.append(f"- issues: {doc['issues']}")
        deps = frontmatter.get("dependencies") or []
        links = frontmatter.get("linked_docs") or []
        if deps:
            lines.append(f"- deps: {deps}")
        if links:
            lines.append(f"- linked_docs: {links}")
        lines.append("")

    markdown_path = artefacts_dir / "screening_report.md"
    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    return markdown_path


def main() -> None:
    """Entry point that mirrors the governance screening command."""

    markdown_path = write_reports(Path("."))
    print(
        "Wrote artefacts/screening_report.json and",
        markdown_path.name,
        "in",
        markdown_path.parent,
    )


if __name__ == "__main__":
    main()
