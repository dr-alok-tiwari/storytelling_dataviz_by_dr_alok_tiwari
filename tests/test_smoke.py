"""End-to-end smoke tests for the Streamlit teaching app."""

from __future__ import annotations

import pandas as pd
from streamlit.testing.v1 import AppTest

from modules.data_generators import DATASETS


PAGES = [
    "Home",
    "Roadmap",
    *[f"S{i}" for i in range(1, 17)],
    "Engine",
    "Story",
    "Cases",
    "Quiz",
    "Resources",
]


def _assert_clean_run(app: AppTest, page: str) -> None:
    exceptions = list(app.exception)
    assert not exceptions, f"Page {page!r} raised: {[str(exc.value) for exc in exceptions]}"


def test_all_synthetic_datasets_generate_successfully() -> None:
    for name, loader in DATASETS.items():
        frame = loader()
        assert isinstance(frame, pd.DataFrame), f"{name} did not return a DataFrame"
        assert not frame.empty, f"{name} returned an empty DataFrame"


def test_every_app_page_renders_without_exception() -> None:
    app = AppTest.from_file("app.py", default_timeout=90)
    app.run(timeout=90)
    _assert_clean_run(app, "Home")

    for page in PAGES:
        app.session_state["page"] = page
        app.run(timeout=90)
        _assert_clean_run(app, page)
