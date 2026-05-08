"""
home.py
Landing page, course roadmap, and course overview.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from modules.ui_components import (
    callout_insight, footer, PRIMARY, ACCENT, SUCCESS, DANGER,
    SESSION_TITLES, SESSION_MODULE, MODULE_LABELS, MODULE_COLORS, SESSION_CLO
)

WARNING = "#E67E22"


def render_home():
    st.markdown("""
    <div class="hero-strip">
        <h1>📊 Storytelling using Data Visualization</h1>
        <p>PGDM-BDA Core Course &nbsp;·&nbsp; 2 Credits &nbsp;·&nbsp; 16 Sessions × 75 Minutes
        &nbsp;·&nbsp; Goa Institute of Management</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### About This Course")
        st.write("""
        Data without communication is noise. This course teaches PGDM-BDA students
        how to transform analysis into decisions — by selecting the right chart,
        designing honest and clear visuals, and building narratives that move people
        from 'interesting data' to 'clear action'.

        By the end, you will be able to critique a weak dashboard, redesign a
        misleading chart, and build a complete visual story from raw data to
        a board-ready recommendation.
        """)
        st.markdown("### 🎓 Instructor")
        st.markdown("**Dr. Alok Tiwari** — Assistant Professor, Big Data Analytics")
        st.markdown("Goa Institute of Management, Panaji, Goa")
        st.markdown("*PhD (Biomedical Engineering, IIT-BHU) · Research: Medical Imaging AI, MLOps, Healthcare Analytics*")

    with col2:
        st.markdown("### 📋 How to Use This App")
        steps = [
            ("Sidebar", "Navigate to any session or tool"),
            ("Concept tab", "Read the concept explanation"),
            ("Demo tab", "Interact with live charts"),
            ("Lab tab", "Complete hands-on activities"),
            ("Quiz tab", "Test your knowledge"),
            ("Reflect tab", "Apply to your context"),
        ]
        for label, desc in steps:
            st.markdown(f"**{label}** — {desc}")

    st.markdown("---")
    st.markdown("### 🎯 Course Learning Outcomes")
    clos = [
        ("CLO1", "Explain the role of data visualization in presenting analytics-driven solutions to management problems.", "🔍"),
        ("CLO2", "Select and design appropriate charts, dashboards, and visual layouts for different business contexts.", "📐"),
        ("CLO3", "Construct coherent and decision-oriented narratives from data using visualization tools and frameworks.", "📖"),
        ("CLO4", "Communicate business insights and strategic recommendations effectively through visual stories.", "🎯"),
    ]
    cols = st.columns(4)
    for col, (clo, desc, icon) in zip(cols, clos):
        col.markdown(f"""
        <div style="background:white;border:1px solid #E2EAF4;border-radius:10px;
                    padding:1rem;text-align:center;border-top:4px solid {PRIMARY};
                    box-shadow:0 2px 6px rgba(0,0,0,0.06);height:180px;">
        <div style="font-size:1.8rem;">{icon}</div>
        <div style="font-weight:700;color:{PRIMARY};font-size:1rem;">{clo}</div>
        <div style="font-size:0.82rem;color:#4B5563;margin-top:0.4rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📅 16-Session Course Roadmap")
    mod_cols = st.columns(4)
    for mod_num, col in enumerate(mod_cols, 1):
        sessions = [s for s, m in SESSION_MODULE.items() if m == mod_num]
        color = MODULE_COLORS[mod_num]
        col.markdown(f"""
        <div style="background:{color};color:white;border-radius:8px;padding:0.6rem 0.8rem;
                    font-weight:600;font-size:0.88rem;margin-bottom:0.5rem;">
        {MODULE_LABELS[mod_num]}
        </div>
        """, unsafe_allow_html=True)
        for s in sessions:
            col.markdown(f"""
            <div style="background:white;border:1px solid #E2EAF4;border-left:3px solid {color};
                        border-radius:6px;padding:0.5rem 0.7rem;margin-bottom:0.4rem;font-size:0.8rem;">
            <strong style="color:{color};">S{s}</strong> — {SESSION_TITLES[s]}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🗺 CLO-Session Mapping")
    mapping_df = pd.DataFrame({
        "Session": list(SESSION_TITLES.keys()),
        "Topic": list(SESSION_TITLES.values()),
        "Module": [MODULE_LABELS[SESSION_MODULE[s]] for s in SESSION_TITLES],
        "CLO": [SESSION_CLO[s] for s in SESSION_TITLES],
    })
    st.dataframe(mapping_df, use_container_width=True, hide_index=True)


def render_roadmap():
    st.markdown("""
    <div class="hero-strip">
        <h1>🗺 Course Roadmap</h1>
        <p>Interactive overview of all 16 sessions — topics, modules, and CLO mapping.</p>
    </div>
    """, unsafe_allow_html=True)

    # Timeline chart
    sessions = list(SESSION_TITLES.keys())
    titles = [f"S{s}: {SESSION_TITLES[s][:35]}..." if len(SESSION_TITLES[s]) > 35
              else f"S{s}: {SESSION_TITLES[s]}" for s in sessions]
    modules = [SESSION_MODULE[s] for s in sessions]
    colors = [MODULE_COLORS[m] for m in modules]
    clos = [SESSION_CLO[s] for s in sessions]

    fig = go.Figure()
    for i, (s, title, color, clo) in enumerate(zip(sessions, titles, colors, clos)):
        fig.add_trace(go.Scatter(
            x=[i + 1], y=[SESSION_MODULE[s]],
            mode="markers+text",
            marker=dict(size=32, color=color, symbol="circle",
                        line=dict(color="white", width=2)),
            text=[str(s)],
            textfont=dict(color="white", size=12, family="Inter"),
            textposition="middle center",
            hovertext=f"Session {s}: {SESSION_TITLES[s]}<br>{clo}",
            hoverinfo="text",
            showlegend=False,
        ))

    fig.update_layout(
        title="Course Journey — 16 Sessions Across 4 Modules",
        xaxis=dict(title="Session Number", tickvals=list(range(1, 17)),
                   ticktext=[str(i) for i in range(1, 17)]),
        yaxis=dict(title="Module", tickvals=[1, 2, 3, 4],
                   ticktext=["M1: Foundations", "M2: Dashboard", "M3: Storytelling", "M4: Strategy"]),
        height=380, plot_bgcolor="#F8FAFC",
    )

    # Add module background bands
    for mod, (y0, y1, color, label) in enumerate(
        [(0.5, 1.5, "#EBF5FB", "Foundations"),
         (1.5, 2.5, "#E9F7EF", "Dashboard"),
         (2.5, 3.5, "#F5EEF8", "Storytelling"),
         (3.5, 4.5, "#FDEDEC", "Strategy")], 1
    ):
        fig.add_hrect(y0=y0, y1=y1, fillcolor=color, line_width=0, layer="below")

    st.plotly_chart(fig, use_container_width=True)
    callout_insight("The course builds progressively: foundations → design → storytelling → strategy. Each module's sessions are scaffolded so later sessions assume earlier learning.", "Scaffolded Design")

    # 75-minute session flow
    st.markdown("### ⏱ Typical 75-Minute Session Flow")
    flow = [
        ("0–5 min", "Warm-up / Prior session recap", SUCCESS),
        ("5–20 min", "Concept explanation + class discussion", PRIMARY),
        ("20–40 min", "Live demo + guided chart building", "#7D3C98"),
        ("40–60 min", "Lab exercise (individual or group)", WARNING),
        ("60–70 min", "Class discussion + critique", ACCENT),
        ("70–75 min", "Quiz + reflection", DANGER),
    ]
    for time, activity, color in flow:
        st.markdown(f"""
        <div style="display:flex;align-items:center;margin-bottom:0.5rem;">
        <div style="background:{color};color:white;border-radius:4px;padding:0.2rem 0.6rem;
                    font-size:0.8rem;min-width:90px;text-align:center;font-weight:600;">{time}</div>
        <div style="margin-left:0.8rem;font-size:0.9rem;">{activity}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📊 Assessment Alignment")
    assess = pd.DataFrame({
        "Component": ["In-class Quizzes (5)", "Mini-Labs (8)", "Business Case Analysis (3)", "Final Visual Story Project", "Class Participation"],
        "Weight": ["15%", "20%", "25%", "30%", "10%"],
        "CLOs Assessed": ["CLO1, CLO2", "CLO2, CLO3", "CLO3, CLO4", "CLO1–CLO4", "All CLOs"],
    })
    st.dataframe(assess, use_container_width=True, hide_index=True)
