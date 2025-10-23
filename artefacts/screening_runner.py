"""Utilities for governance screening tasks.

This module currently focuses on two areas:
* Ensuring CODEOWNERS coverage for key directories with normalized handles.
* Collecting Markdown artefacts while allowing CI to ignore volatile paths via
  an environment whitelist.

Both helpers are intentionally lightweight so that they can run inside simple
CI jobs without extra dependencies.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Iterable, List

OWNER_REQ = "stephan-adod"


def _normalize_handle(value: str | None) -> str | None:
    """Return the canonical representation of a CODEOWNERS handle.

    CODEOWNERS entries often start with an ``@`` when referencing GitHub
    handles.  The governance rules we enforce only care about the underlying
    identifier, so we strip the sigil to make comparisons stable.
    """

    if value is None:
        return None
    return value.lstrip("@")


def _parse_codeowners(codeowners_path: Path) -> Dict[str, List[str]]:
    """Parse the CODEOWNERS file into a mapping of pattern → owners.

    The function keeps the original ordering of patterns but normalizes owner
    handles to make downstream comparisons insensitive to ``@`` prefixes.
    """

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
    """Check whether required CODEOWNERS coverage exists for select patterns.

    Parameters
    ----------
    base_path:
        Directory that contains the ``CODEOWNERS`` file.  In CI this defaults
        to the repository root, but tests can inject a temporary directory.
    required_owner:
        The canonical owner identifier that must appear in every monitored
        pattern.  Handles inside the file may contain an ``@`` prefix—they are
        normalized before comparison.
    patterns:
        Optional iterable of path patterns that must include ``required_owner``.
        Defaults to ``("meta/*", "artefacts/*")``.

    Returns
    -------
    dict
        A dictionary describing the evaluation, including the parsed rules and
        a list of any issues that were detected.  The shape intentionally
        mirrors the previous runner implementation for backwards compatibility.
    """

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
    """Collect Markdown files while respecting the CI ignore whitelist.

    The environment variable ``GOV_IGNORE_PATTERNS`` accepts a semicolon
    separated list of substrings.  Any Markdown file whose path contains one of
    the substrings will be excluded from the result.  This gives CI pipelines a
    simple escape hatch to avoid volatile fixtures.
    """

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


def main() -> None:
    """Entry point for ad-hoc smoke checks during development."""

    result = check_codeowners()
    print("CODEOWNERS report:", result)

    base = Path(".")
    markdowns = collect_markdowns(base)
    print(f"Found {len(markdowns)} Markdown files under {base!s}.")


if __name__ == "__main__":
    main()
