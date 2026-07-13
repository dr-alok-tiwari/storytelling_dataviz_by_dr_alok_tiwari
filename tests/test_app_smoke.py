from pathlib import Path

from streamlit.testing.v1 import AppTest


def test_home_page_runs_without_exception():
    app_path = Path(__file__).parents[1] / "app.py"
    app = AppTest.from_file(str(app_path), default_timeout=30).run()
    assert not app.exception
