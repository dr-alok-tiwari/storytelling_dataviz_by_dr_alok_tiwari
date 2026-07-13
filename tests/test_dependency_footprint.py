from pathlib import Path


def test_statsmodels_is_not_a_runtime_dependency() -> None:
    root = Path(__file__).parents[1]
    requirements = (root / "requirements.txt").read_text(encoding="utf-8").lower()
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8").lower()
    assert "statsmodels" not in requirements
    assert '"statsmodels' not in pyproject
