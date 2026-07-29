"""Tests for official course-presentation metadata and assets."""

from __future__ import annotations

from pathlib import Path
from zipfile import BadZipFile, ZipFile

import pytest

from modules.session_resources import (
    REPOSITORY_ROOT,
    SESSION_PRESENTATIONS,
    get_session_presentation,
)
from modules.ui_components import SESSION_TITLES


def test_mapping_contains_exactly_sessions_1_to_16() -> None:
    assert set(SESSION_PRESENTATIONS) == set(range(1, 17))
    assert len(SESSION_PRESENTATIONS) == 16


def test_paths_and_download_names_are_unique() -> None:
    paths = [item.path for item in SESSION_PRESENTATIONS.values()]
    names = [item.download_name for item in SESSION_PRESENTATIONS.values()]
    assert len(paths) == len(set(paths))
    assert len(names) == len(set(names))


@pytest.mark.parametrize("session_number", range(1, 17))
def test_each_presentation_is_a_valid_nonempty_pptx(session_number: int) -> None:
    item = get_session_presentation(session_number)
    path = REPOSITORY_ROOT / item.path
    assert path.exists()
    assert path.is_file()
    assert path.stat().st_size > 0
    assert path.suffix.lower() == ".pptx"
    assert path.read_bytes()[:2] == b"PK"
    try:
        with ZipFile(path) as archive:
            names = set(archive.namelist())
    except BadZipFile as exc:
        raise AssertionError(f"Invalid PPTX archive: {path}") from exc
    assert "[Content_Types].xml" in names
    assert "ppt/presentation.xml" in names


@pytest.mark.parametrize("session_number", range(1, 17))
def test_titles_use_canonical_application_metadata(session_number: int) -> None:
    assert SESSION_PRESENTATIONS[session_number].title == SESSION_TITLES[session_number]


@pytest.mark.parametrize("invalid", [0, 17, -1, 1.0, "1", True, None])
def test_invalid_session_numbers_are_rejected(invalid: object) -> None:
    with pytest.raises(ValueError, match="1 to 16"):
        get_session_presentation(invalid)  # type: ignore[arg-type]


def test_resource_module_has_no_network_dependency() -> None:
    source = Path(__file__).parents[1].joinpath("modules/session_resources.py").read_text()
    forbidden = ("requests.", "httpx.", "urllib.request", "socket.")
    assert not any(token in source for token in forbidden)
