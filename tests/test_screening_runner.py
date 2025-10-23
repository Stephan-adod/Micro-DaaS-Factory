from pathlib import Path


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
