"""Production entry point for the Storytelling using Data Visualization app."""

from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="DataViz Storytelling | GIM BDA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "Storytelling using Data Visualization — an interactive PGDM-BDA "
            "teaching application developed by Dr. Alok Tiwari at Goa Institute "
            "of Management. All datasets are synthetic."
        )
    },
)

from modules.home import render_home, render_roadmap
from modules.sessions_1_8 import (
    session_1,
    session_2,
    session_3,
    session_4,
    session_5,
    session_6,
    session_7,
    session_8,
)
from modules.sessions_9_16 import (
    session_9,
    session_10,
    session_11,
    session_12,
    session_13,
    session_14,
    session_15,
    session_16,
)
from modules.tools import (
    render_case_library,
    render_chart_engine,
    render_quiz_zone,
    render_resources,
    render_storytelling_builder,
)
from modules.ui_components import footer, inject_css


APP_VERSION = "2.0.0"


def _initialise_state() -> None:
    """Create cross-page session state used by progress and accessibility controls."""
    if "completed" not in st.session_state:
        st.session_state.completed = {i: False for i in range(1, 17)}
    else:
        st.session_state.completed = {
            i: bool(st.session_state.completed.get(i, False)) for i in range(1, 17)
        }

    st.session_state.setdefault("classroom_mode", False)
    st.session_state.setdefault("reduce_motion", False)


_initialise_state()

home_page = st.Page(
    render_home,
    title="Home",
    icon=":material/home:",
    default=True,
)
roadmap_page = st.Page(
    render_roadmap,
    title="Course roadmap",
    icon=":material/route:",
    url_path="course-roadmap",
)

session_pages = {
    1: st.Page(session_1, title="1. Why visualization matters", icon="📖", url_path="session-01"),
    2: st.Page(session_2, title="2. Mapping data to visuals", icon="🔗", url_path="session-02"),
    3: st.Page(session_3, title="3. Axes, scales & coordinates", icon="📐", url_path="session-03"),
    4: st.Page(session_4, title="4. Color & visual attention", icon="🎨", url_path="session-04"),
    5: st.Page(session_5, title="5. Visualizing amounts", icon="📊", url_path="session-05"),
    6: st.Page(session_6, title="6. Distributions & variation", icon="📉", url_path="session-06"),
    7: st.Page(session_7, title="7. Proportions & composition", icon="🥧", url_path="session-07"),
    8: st.Page(session_8, title="8. Critiquing weak stories", icon="🔍", url_path="session-08"),
    9: st.Page(session_9, title="9. Relationships & insight", icon="🔁", url_path="session-09"),
    10: st.Page(session_10, title="10. Time series & change", icon="📈", url_path="session-10"),
    11: st.Page(session_11, title="11. Dashboard storytelling", icon="🖥️", url_path="session-11"),
    12: st.Page(session_12, title="12. Titles, annotation & flow", icon="✏️", url_path="session-12"),
    13: st.Page(session_13, title="13. Storytelling pitfalls", icon="⚠️", url_path="session-13"),
    14: st.Page(session_14, title="14. Strategy communication", icon="♟️", url_path="session-14"),
    15: st.Page(session_15, title="15. Integrated workshop", icon="🔧", url_path="session-15"),
    16: st.Page(session_16, title="16. Healthcare DataViz", icon="🏥", url_path="session-16"),
}

tool_pages = {
    "chart": st.Page(
        render_chart_engine,
        title="Chart selection engine",
        icon=":material/insert_chart:",
        url_path="chart-selection-engine",
    ),
    "story": st.Page(
        render_storytelling_builder,
        title="Storytelling builder",
        icon=":material/edit_note:",
        url_path="storytelling-builder",
    ),
    "cases": st.Page(
        render_case_library,
        title="Business case library",
        icon=":material/library_books:",
        url_path="business-cases",
    ),
    "quiz": st.Page(
        render_quiz_zone,
        title="Quiz zone",
        icon=":material/quiz:",
        url_path="quiz-zone",
    ),
    "resources": st.Page(
        render_resources,
        title="Resources & tools",
        icon=":material/construction:",
        url_path="resources",
    ),
}

pages = {
    "": [home_page, roadmap_page],
    "Module 1 · Foundations": [session_pages[i] for i in range(1, 5)],
    "Module 2 · Dashboard design": [session_pages[i] for i in range(5, 9)],
    "Module 3 · Storytelling": [session_pages[i] for i in range(9, 13)],
    "Module 4 · Business applications": [session_pages[i] for i in range(13, 17)],
    "Practice tools": list(tool_pages.values()),
}

# Make page objects available to Home and shared session controls without circular imports.
st.session_state["_session_pages"] = session_pages
st.session_state["_tool_pages"] = tool_pages
st.session_state["_roadmap_page"] = roadmap_page

current_page = st.navigation(pages, position="top")

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">📊</div>
            <div>
                <div class="sidebar-brand-title">DataViz Storytelling</div>
                <div class="sidebar-brand-subtitle">PGDM-BDA · GIM Goa</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    completed_count = sum(st.session_state.completed.values())
    st.markdown("#### Course progress")
    st.progress(completed_count / 16, text=f"{completed_count} of 16 sessions completed")

    next_session = next(
        (number for number, done in st.session_state.completed.items() if not done),
        None,
    )
    if next_session is not None:
        st.page_link(
            session_pages[next_session],
            label=f"Continue with Session {next_session}",
            icon=":material/play_arrow:",
            use_container_width=True,
        )
    else:
        st.success("All sessions completed!", icon="🏆")

    st.divider()
    st.markdown("#### Display")
    st.toggle(
        "Classroom mode",
        key="classroom_mode",
        help="Enlarges body text, controls, tabs, and chart labels for projection.",
    )
    st.toggle(
        "Reduce motion",
        key="reduce_motion",
        help="Disables non-essential transitions and animations.",
    )

    with st.expander("Progress options"):
        if st.button("Reset course progress", use_container_width=True):
            st.session_state.completed = {i: False for i in range(1, 17)}
            for i in range(1, 17):
                st.session_state.pop(f"session_complete_{i}", None)
            st.rerun()
        st.caption("Progress is stored only for the current browser session.")

    st.divider()
    st.caption(f"Version {APP_VERSION} · Synthetic educational data")

inject_css(
    classroom_mode=st.session_state.classroom_mode,
    reduce_motion=st.session_state.reduce_motion,
)

current_page.run()
footer()
