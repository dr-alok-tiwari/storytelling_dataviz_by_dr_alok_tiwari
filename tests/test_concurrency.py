"""Concurrency and resource-safety tests for the Streamlit application."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import plotly.express as px
from streamlit.testing.v1 import AppTest

from modules.data_generators import scatter_sales_spend
from modules.tools_runtime_patch import install


LAZY_TAB_SCRIPT = """
import streamlit as st
from modules.lazy_tabs import enable_lazy_tabs


def legacy_page():
    first, second = st.tabs(["First", "Second"])
    with first:
        st.session_state["first_runs"] = st.session_state.get("first_runs", 0) + 1
        st.write("First tab content")
    with second:
        st.session_state["second_runs"] = st.session_state.get("second_runs", 0) + 1
        st.write("Second tab content")


enable_lazy_tabs(legacy_page, key="demo_tabs")()
"""


STRESS_SCRIPT = """
import streamlit as st
from modules.lazy_tabs import enable_lazy_tabs
from modules.sessions_9_16 import session_11
from modules.tools_runtime_patch import install

install()
st.session_state.setdefault("completed", {i: False for i in range(1, 17)})
enable_lazy_tabs(session_11, key="stress_tabs")()
"""


def test_hidden_tab_bodies_are_not_executed() -> None:
    app = AppTest.from_string(LAZY_TAB_SCRIPT, default_timeout=60).run()
    assert not app.exception
    assert app.session_state["first_runs"] == 1
    assert "second_runs" not in app.session_state

    app.session_state["demo_tabs"] = "Second"
    app.run(timeout=60)
    assert not app.exception
    assert app.session_state["second_runs"] == 1


def test_numpy_ols_trendlines_work_without_statsmodels() -> None:
    install()
    figure = px.scatter(
        scatter_sales_spend(),
        x="marketing_spend",
        y="revenue",
        color="channel",
        trendline="ols",
    )
    trend_traces = [trace for trace in figure.data if str(trace.name).endswith(" trend")]
    assert len(trend_traces) == 3


def _run_heavy_session() -> None:
    app = AppTest.from_string(STRESS_SCRIPT, default_timeout=120).run(timeout=120)
    assert not app.exception

    # Force the chart-heavy dashboard demo tab and rerun the same isolated session.
    app.session_state["stress_tabs"] = "📊 Demo"
    app.run(timeout=120)
    assert not app.exception


def test_eight_simultaneous_streamlit_sessions() -> None:
    """Exercise independent session state and chart rendering concurrently."""

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(_run_heavy_session) for _ in range(8)]
        for future in futures:
            future.result(timeout=180)
