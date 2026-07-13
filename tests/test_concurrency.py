"""Concurrency and resource-safety tests for the Streamlit application."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import plotly.express as px
from streamlit.testing.v1 import AppTest

from modules.data_generators import (
    bed_occupancy,
    regional_sales,
    retail_sales,
    scatter_sales_spend,
)
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


def test_hidden_tab_bodies_are_not_executed() -> None:
    app = AppTest.from_string(LAZY_TAB_SCRIPT, default_timeout=60).run()
    assert not app.exception
    assert app.session_state["first_runs"] == 1
    assert "second_runs" not in app.session_state

    app.session_state["demo_tabs"] = "Second"
    app.run(timeout=60)
    assert not app.exception
    assert app.session_state["second_runs"] == 1


def test_streamlit_sessions_keep_independent_state() -> None:
    first_user = AppTest.from_string(LAZY_TAB_SCRIPT, default_timeout=60).run()
    second_user = AppTest.from_string(LAZY_TAB_SCRIPT, default_timeout=60).run()

    first_user.session_state["private_marker"] = "first-user-only"
    first_user.run(timeout=60)

    assert first_user.session_state["private_marker"] == "first-user-only"
    assert "private_marker" not in second_user.session_state


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


def _run_chart_heavy_workload(worker_id: int) -> tuple[int, int, int]:
    """Build the main dashboard chart families using shared cached data."""

    install()

    occupancy = bed_occupancy()
    occupancy_recent = occupancy[
        occupancy["date"] >= occupancy["date"].max() - occupancy["date"].max().freq.delta
    ] if getattr(occupancy["date"].max(), "freq", None) else occupancy.tail(150)
    occupancy_trend = occupancy_recent.groupby(["date", "ward"], as_index=False)["occupancy_pct"].mean()
    occupancy_figure = px.line(
        occupancy_trend,
        x="date",
        y="occupancy_pct",
        color="ward",
        title=f"Occupancy workload {worker_id}",
    )

    sales = regional_sales().groupby("region", as_index=False)["sales"].sum()
    sales_figure = px.bar(sales, x="region", y="sales")

    revenue = retail_sales()
    relationship_figure = px.scatter(
        scatter_sales_spend(),
        x="marketing_spend",
        y="revenue",
        color="channel",
        trendline="ols",
    )

    return (
        len(occupancy_figure.data),
        len(sales_figure.data),
        len(relationship_figure.data) + len(revenue),
    )


def test_eight_simultaneous_chart_render_workloads() -> None:
    """Exercise cached data and chart generation from eight concurrent workers."""

    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(_run_chart_heavy_workload, range(8)))

    assert len(results) == 8
    assert all(occupancy_traces >= 1 for occupancy_traces, _, _ in results)
    assert all(sales_traces >= 1 for _, sales_traces, _ in results)
    assert all(relationship_size > 24 for _, _, relationship_size in results)
