import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_owner_normalization(tmp_path: Path):
    from artefacts.screening_runner import check_codeowners

    codeowners = tmp_path / "CODEOWNERS"
    codeowners.write_text("""
# comment
meta/* @stephan-adod
artefacts/* @stephan-adod
""".strip())

    result = check_codeowners(base_path=tmp_path, required_owner="stephan-adod")
    assert result["issues"] == []


def test_ignore_patterns_env(monkeypatch, tmp_path: Path):
    from artefacts import screening_runner as sr

    nested = tmp_path / "meta" / "_fixtures"
    nested.mkdir(parents=True)
    (nested / "ignore.md").write_text("# ignore")
    (tmp_path / "keep.md").write_text("# keep")

    monkeypatch.setenv("GOV_IGNORE_PATTERNS", "_fixtures/")

    collected = sr.collect_markdowns(tmp_path)
    collected_strs = {str(path) for path in collected}

    assert all("_fixtures" not in path for path in collected_strs)
    assert any(path.endswith("keep.md") for path in collected_strs)


def test_parse_frontmatter(tmp_path: Path):
    from artefacts import screening_runner as sr

    doc = tmp_path / "doc.md"
    doc.write_text(
        """---
title: "Example"
version: "v3.1"
owner: "stephan-adod"
phase: "Recovery"
status: "canonical"
updated: "2024-01-01"
review_due: "2024-03-01"
retention: "12M"
dependencies:
  - "meta/dep.md"
linked_docs:
  - "meta/link.md"
layer: "semantic"
policy_source: "meta/dep.md"
policy_version: "v3.1"
---
body
"""
    )

    frontmatter, err = sr.parse_frontmatter(doc)
    assert err is None
    assert frontmatter["title"] == "Example"
    assert frontmatter["dependencies"] == ["meta/dep.md"]


def test_evaluate_doc_and_report(tmp_path: Path):
    from artefacts import screening_runner as sr

    base = tmp_path
    meta_dir = base / "meta"
    meta_dir.mkdir()

    dependency = meta_dir / "dep.md"
    dependency.write_text(
        """---
title: "Dep"
version: "v3.1"
status: "canonical"
phase: "Recovery"
owner: "stephan-adod"
updated: "2024-01-01"
review_due: "2024-02-15"
retention: "12M"
dependencies: []
linked_docs: []
layer: "semantic"
policy_source: "meta/dep.md"
policy_version: "v3.1"
---
"""
    )

    linked = meta_dir / "link.md"
    linked.write_text(
        """---
title: "Link"
version: "v3.1"
status: "canonical"
phase: "Recovery"
owner: "stephan-adod"
updated: "2024-01-01"
review_due: "2024-02-15"
retention: "12M"
dependencies: []
linked_docs: []
layer: "semantic"
policy_source: "meta/link.md"
policy_version: "v3.1"
---
"""
    )

    doc = meta_dir / "doc.md"
    doc.write_text(
        """---
title: "Doc"
version: "v3.1"
status: "canonical"
phase: "Recovery"
owner: "stephan-adod"
updated: "2024-01-10"
review_due: "2024-03-01"
retention: "12M"
dependencies:
  - "meta/dep.md"
linked_docs:
  - "meta/link.md"
layer: "semantic"
policy_source: "meta/dep.md"
policy_version: "v3.1"
---
"""
    )

    evaluation = sr.evaluate_doc(doc, base)
    assert evaluation.ok
    assert evaluation.frontmatter["dependencies"] == ["meta/dep.md"]

    markdown_path = sr.write_reports(base)
    assert markdown_path.exists()
    json_report = base / "artefacts" / "screening_report.json"
    data = json.loads(json_report.read_text())
    assert data["summary"]["scanned_files"] == 3
