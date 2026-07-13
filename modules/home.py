"""Landing page and course roadmap."""

from __future__ import annotations

from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from modules.ui_components import (
    ACCENT,
    DANGER,
    MODULE_COLORS,
    MODULE_LABELS,
    PRIMARY,
    SESSION_CLO,
    SESSION_MODULE,
    SESSION_TITLES,
    SUCCESS,
    callout_insight,
    hero,
)

WARNING = "#B85C00"


def _completion_summary() -> tuple[int, int | None]:
    completed = st.session_state.get("completed", {i: False for i in range(1, 17)})
    count = sum(bool(completed.get(i, False)) for i in range(1, 17))
    next_session = next((i for i in range(1, 17) if not completed.get(i, False)), None)
    return count, next_session


def _quick_start() -> None:
    completed_count, next_session = _completion_summary()
    session_pages = st.session_state.get("_session_pages", {})
    tool_pages = st.session_state.get("_tool_pages", {})

    st.markdown("### Continue learning")
    progress_col, action_col = st.columns([1.5, 1])
    with progress_col:
        st.progress(
            completed_count / 16,
            text=f"{completed_count} of 16 sessions completed",
        )
        if completed_count == 0:
            st.caption("Begin with Session 1, or use the roadmap to explore the full course.")
        elif completed_count == 16:
            st.success("You have completed the full course.", icon="🏆")
        else:
            st.caption("Progress is stored for the current browser session.")

    with action_col:
        if next_session is not None and next_session in session_pages:
            label = "Start Session 1" if next_session == 1 else f"Continue Session {next_session}"
            st.page_link(
                session_pages[next_session],
                label=label,
                icon=":material/play_arrow:",
                use_container_width=True,
            )
        roadmap_page = st.session_state.get("_roadmap_page")
        if roadmap_page is not None:
            st.page_link(
                roadmap_page,
                label="Open course roadmap",
                icon=":material/route:",
                use_container_width=True,
            )

    if tool_pages:
        st.markdown("#### Practice tools")
        columns = st.columns(3)
        shortcuts = [
            ("chart", "Choose the right chart", ":material/insert_chart:"),
            ("story", "Build a data story", ":material/edit_note:"),
            ("quiz", "Test your knowledge", ":material/quiz:"),
        ]
        for column, (key, label, icon) in zip(columns, shortcuts):
            if key in tool_pages:
                with column:
                    st.page_link(
                        tool_pages[key],
                        label=label,
                        icon=icon,
                        use_container_width=True,
                    )


def render_home() -> None:
    hero(
        "📊 Storytelling using Data Visualization",
        "PGDM-BDA core course · 2 credits · 16 sessions × 75 minutes · Goa Institute of Management",
    )

    _quick_start()
    st.divider()

    about_col, use_col = st.columns([1.6, 1])
    with about_col:
        st.markdown("### About this course")
        st.write(
            """
            Data without communication is noise. This course helps students transform
            analysis into decisions by selecting the right chart, designing honest and
            accessible visuals, and constructing narratives that move an audience from
            **evidence** to **insight** to **action**.

            By the end of the course, students should be able to critique a weak
            dashboard, redesign a misleading chart, and build a complete visual story
            from raw data to a management-ready recommendation.
            """
        )
        st.markdown("#### Instructor")
        st.markdown("**Dr. Alok Tiwari**  ")
        st.markdown("Assistant Professor — Big Data Analytics, Goa Institute of Management")
        st.caption(
            "PhD, Biomedical Engineering (IIT-BHU) · Research interests: medical imaging AI, "
            "MLOps, healthcare analytics, and responsible data communication"
        )

    with use_col:
        st.markdown("### How to use the app")
        steps = [
            ("1", "Learn", "Read the concept and inspect the worked examples."),
            ("2", "Explore", "Change controls and observe how the visual story changes."),
            ("3", "Apply", "Complete the lab using the supplied synthetic dataset."),
            ("4", "Check", "Attempt the quiz before revealing the explanation."),
            ("5", "Reflect", "Record one insight and mark the session complete."),
        ]
        for number, label, description in steps:
            st.markdown(f"**{number}. {label}** — {description}")

    st.divider()
    st.markdown("### Course learning outcomes")
    clos = [
        (
            "CLO1",
            "Explain how data visualization supports analytics-driven management decisions.",
            "🔍",
        ),
        (
            "CLO2",
            "Select and design appropriate charts, dashboards, and visual layouts.",
            "📐",
        ),
        (
            "CLO3",
            "Construct coherent, decision-oriented narratives from data and visual evidence.",
            "📖",
        ),
        (
            "CLO4",
            "Communicate business insights and recommendations through persuasive visual stories.",
            "🎯",
        ),
    ]
    columns = st.columns(4)
    for column, (clo, description, icon) in zip(columns, clos):
        column.markdown(
            f"""
            <div class="content-card" style="border-top:4px solid {PRIMARY}; text-align:center;">
                <div style="font-size:1.8rem;" aria-hidden="true">{icon}</div>
                <div style="font-weight:760;color:{PRIMARY};font-size:1.1rem;">{clo}</div>
                <div style="font-size:.95rem;color:#405267;margin-top:.45rem;line-height:1.5;">
                    {escape(description)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown("### Four-module learning journey")
    session_pages = st.session_state.get("_session_pages", {})
    module_columns = st.columns(4)
    for module_number, column in enumerate(module_columns, 1):
        color = MODULE_COLORS[module_number]
        sessions = [session for session, module in SESSION_MODULE.items() if module == module_number]
        with column:
            st.markdown(
                f"""
                <div style="background:{color};color:white;border-radius:.65rem;padding:.7rem .85rem;
                            font-weight:720;margin-bottom:.55rem;">
                    {escape(MODULE_LABELS[module_number])}
                </div>
                """,
                unsafe_allow_html=True,
            )
            for session in sessions:
                if session in session_pages:
                    st.page_link(
                        session_pages[session],
                        label=f"S{session}: {SESSION_TITLES[session]}",
                        use_container_width=True,
                    )

    st.divider()
    st.markdown("### CLO–session mapping")
    mapping_df = pd.DataFrame(
        {
            "Session": list(SESSION_TITLES),
            "Topic": list(SESSION_TITLES.values()),
            "Module": [MODULE_LABELS[SESSION_MODULE[s]] for s in SESSION_TITLES],
            "CLO": [SESSION_CLO[s] for s in SESSION_TITLES],
        }
    )
    st.dataframe(mapping_df, use_container_width=True, hide_index=True)
    st.caption("All examples and downloadable datasets in the app are synthetic and intended for education.")


def render_roadmap() -> None:
    hero(
        "🗺 Course Roadmap",
        "A progressive 16-session journey from visual foundations to strategic and healthcare applications.",
    )

    sessions = list(SESSION_TITLES)
    modules = [SESSION_MODULE[session] for session in sessions]
    colors = [MODULE_COLORS[module] for module in modules]

    figure = go.Figure()
    for index, (session, color) in enumerate(zip(sessions, colors), start=1):
        figure.add_trace(
            go.Scatter(
                x=[index],
                y=[SESSION_MODULE[session]],
                mode="markers+text",
                marker={
                    "size": 34,
                    "color": color,
                    "symbol": "circle",
                    "line": {"color": "white", "width": 2},
                },
                text=[str(session)],
                textfont={"color": "white", "size": 13},
                textposition="middle center",
                hovertemplate=(
                    f"<b>Session {session}</b><br>{SESSION_TITLES[session]}"
                    f"<br>{SESSION_CLO[session]}<extra></extra>"
                ),
                showlegend=False,
            )
        )

    bands = [
        (0.5, 1.5, "#EAF3FB"),
        (1.5, 2.5, "#E7F6F2"),
        (2.5, 3.5, "#F2EAF7"),
        (3.5, 4.5, "#F9ECE9"),
    ]
    for lower, upper, color in bands:
        figure.add_hrect(y0=lower, y1=upper, fillcolor=color, line_width=0, layer="below")

    figure.update_layout(
        title="Course journey — 16 sessions across 4 modules",
        xaxis={
            "title": "Session number",
            "tickvals": list(range(1, 17)),
            "ticktext": [str(i) for i in range(1, 17)],
        },
        yaxis={
            "title": "Module",
            "tickvals": [1, 2, 3, 4],
            "ticktext": ["M1: Foundations", "M2: Dashboard", "M3: Storytelling", "M4: Strategy"],
        },
        height=430,
        plot_bgcolor="#FFFFFF",
        margin={"t": 65, "r": 20, "b": 55, "l": 80},
        hoverlabel={"font_size": 14},
    )
    st.plotly_chart(figure, use_container_width=True, config={"displaylogo": False})

    callout_insight(
        "The course is deliberately scaffolded: perceptual foundations → chart and dashboard design "
        "→ narrative construction → strategic application. Later sessions assume earlier skills.",
        "Scaffolded design",
    )

    flow_col, assessment_col = st.columns([1.1, 1])
    with flow_col:
        st.markdown("### Typical 75-minute session")
        flow = [
            ("0–5 min", "Warm-up and prior-session retrieval", SUCCESS),
            ("5–20 min", "Concept explanation and discussion", PRIMARY),
            ("20–40 min", "Live demonstration and guided exploration", "#6D3A8D"),
            ("40–60 min", "Individual or group lab", WARNING),
            ("60–70 min", "Critique and managerial interpretation", ACCENT),
            ("70–75 min", "Quiz, reflection, and completion", DANGER),
        ]
        for time_range, activity, color in flow:
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:.8rem;margin-bottom:.55rem;">
                    <div style="background:{color};color:white;border-radius:.4rem;padding:.3rem .65rem;
                                min-width:92px;text-align:center;font-weight:700;">{time_range}</div>
                    <div>{escape(activity)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with assessment_col:
        st.markdown("### Assessment alignment")
        assessment = pd.DataFrame(
            {
                "Component": [
                    "In-class quizzes (5)",
                    "Mini-labs (8)",
                    "Business case analyses (3)",
                    "Final visual-story project",
                    "Class participation",
                ],
                "Weight": ["15%", "20%", "25%", "30%", "10%"],
                "CLOs": ["CLO1–2", "CLO2–3", "CLO3–4", "CLO1–4", "All"],
            }
        )
        st.dataframe(assessment, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### Open any session")
    session_pages = st.session_state.get("_session_pages", {})
    for module_number in range(1, 5):
        with st.expander(MODULE_LABELS[module_number], expanded=module_number == 1):
            module_sessions = [s for s in sessions if SESSION_MODULE[s] == module_number]
            columns = st.columns(2)
            for index, session in enumerate(module_sessions):
                if session in session_pages:
                    with columns[index % 2]:
                        st.page_link(
                            session_pages[session],
                            label=f"Session {session}: {SESSION_TITLES[session]}",
                            icon=":material/arrow_forward:",
                            use_container_width=True,
                        )
