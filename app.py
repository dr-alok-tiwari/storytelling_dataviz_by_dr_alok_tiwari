"""
Storytelling using Data Visualization
PGDM-BDA Term 1 — Goa Institute of Management
Interactive Teaching App · Dr. Alok Tiwari
"""

import streamlit as st

st.set_page_config(
    page_title="DataViz Storytelling | GIM BDA",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from modules.ui_components import inject_css, footer
from modules.home import render_home, render_roadmap
from modules.sessions_1_8 import (
    session_1, session_2, session_3, session_4,
    session_5, session_6, session_7, session_8,
)
from modules.sessions_9_16 import (
    session_9,  session_10, session_11, session_12,
    session_13, session_14, session_15, session_16,
)
from modules.tools import (
    render_chart_engine, render_storytelling_builder,
    render_case_library, render_quiz_zone, render_resources,
)

inject_css()

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR CSS  — pure st.button styling, no overlay tricks
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Sidebar background ───────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #0D2137 !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

/* ── Every sidebar button: base style ────────────────── */
section[data-testid="stSidebar"] .stButton > button {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;   /* LEFT-ALIGN text */
    gap: 8px !important;
    width: 100% !important;
    padding: 9px 14px !important;
    margin: 1px 0 !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    background: rgba(255,255,255,0.05) !important;
    color: #CBD5E1 !important;
    font-size: 0.87rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    line-height: 1.35 !important;
    white-space: normal !important;
    word-break: break-word !important;
    transition: background 0.15s, color 0.15s !important;
    box-shadow: none !important;
}

/* ── Hover ────────────────────────────────────────────── */
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.12) !important;
    color: #FFFFFF !important;
    border-color: rgba(255,255,255,0.18) !important;
}

/* ── Active page button (data attribute set via st.button type trick) */
/* We use a CSS class injected on the container div instead */
section[data-testid="stSidebar"] .stButton > button[data-active="true"],
section[data-testid="stSidebar"] .nav-active .stButton > button {
    background: #2563EB !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border-color: #3B82F6 !important;
}

/* ── Module label paragraphs ──────────────────────────── */
section[data-testid="stSidebar"] p.mod-label {
    font-size: 0.67rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
    color: #475569 !important;
    padding: 10px 6px 3px 6px !important;
    margin: 0 !important;
}

/* ── Divider ──────────────────────────────────────────── */
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.08) !important;
    margin: 8px 0 !important;
}

/* ── Progress text ────────────────────────────────────── */
section[data-testid="stSidebar"] .prog-label {
    font-size: 0.75rem !important;
    color: #94A3B8 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "completed" not in st.session_state:
    st.session_state.completed = {i: False for i in range(1, 17)}
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ── Nav data ──────────────────────────────────────────────────────────────────
MODULES = [
    ("Module 1 — Foundations", [
        ("S1",  "📖 Why Visualization Matters",       1),
        ("S2",  "🔗 Mapping Data to Visual Forms",    2),
        ("S3",  "📐 Axes, Scales & Coordinates",      3),
        ("S4",  "🎨 Color, Emphasis & Attention",     4),
    ]),
    ("Module 2 — Dashboard Design", [
        ("S5",  "📊 Visualizing Amounts",             5),
        ("S6",  "📉 Distributions & Variation",       6),
        ("S7",  "🥧 Proportions & Composition",       7),
        ("S8",  "🔍 Critiquing Weak Visual Stories",  8),
    ]),
    ("Module 3 — Storytelling", [
        ("S9",  "🔁 Relationships & Insight",          9),
        ("S10", "📈 Time Series & Change",            10),
        ("S11", "🖥️ Dashboard Storytelling",          11),
        ("S12", "✏️ Annotation, Titles & Narrative",  12),
    ]),
    ("Module 4 — Business Applications", [
        ("S13", "⚠️ Pitfalls in Data Storytelling",  13),
        ("S14", "♟️ Strategy Communication",           14),
        ("S15", "🔧 Integrated Workshop",             15),
        ("S16", "🏥 Healthcare DataViz",              16),
    ]),
]

TOOLS = [
    ("Engine",    "🧭 Chart Selection Engine"),
    ("Story",     "📝 Storytelling Builder"),
    ("Cases",     "📚 Business Case Library"),
    ("Quiz",      "❓ Quiz Zone"),
    ("Resources", "🛠️ Resources & Tools"),
]


def nav_btn(key, label, snum=None):
    """Plain st.button. Active styling injected via surrounding div."""
    is_active = st.session_state.page == key
    done_mark = " ✓" if snum and st.session_state.completed.get(snum) else ""
    display = label + done_mark

    # Wrap in a div with class for CSS targeting
    active_class = "nav-active" if is_active else "nav-inactive"
    st.markdown(f'<div class="{active_class}">', unsafe_allow_html=True)

    # Active button gets a type="primary" for visual distinction
    btn_type = "primary" if is_active else "secondary"
    if st.button(display, key=f"nb_{key}", use_container_width=True, type=btn_type):
        st.session_state.page = key
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def section_label(text):
    st.markdown(f'<p class="mod-label">{text}</p>', unsafe_allow_html=True)


# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown("""
    <div style='text-align:center;padding:16px 8px 12px;
                border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:6px;'>
        <div style='font-size:2rem;line-height:1.1;'>📊</div>
        <div style='font-size:0.98rem;font-weight:700;color:#E2E8F0;margin:6px 0 2px;'>
            DataViz Storytelling</div>
        <div style='font-size:0.73rem;color:#64748B;'>PGDM-BDA &nbsp;|&nbsp; GIM Goa</div>
    </div>""", unsafe_allow_html=True)

    nav_btn("Home",    "🏠 Home")
    nav_btn("Roadmap", "🗺️ Course Roadmap")

    for mod_label, items in MODULES:
        section_label(mod_label)
        for key, label, snum in items:
            nav_btn(key, label, snum)

    section_label("Tools &amp; Resources")
    for key, label in TOOLS:
        nav_btn(key, label)

    # Progress
    done_count = sum(st.session_state.completed.values())
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        f'<p class="prog-label" style="color:#94A3B8;font-size:.75rem;'
        f'padding:2px 4px;">Sessions completed: '
        f'<strong style="color:#E2E8F0;">{done_count} / 16</strong></p>',
        unsafe_allow_html=True,
    )
    st.progress(done_count / 16)
    if done_count == 16:
        st.success("🎉 All 16 sessions complete!", icon="🏆")

# ── Router ────────────────────────────────────────────────────────────────────
RENDER_MAP = {
    "Home":    render_home,
    "Roadmap": render_roadmap,
    "S1": session_1,  "S2": session_2,  "S3": session_3,  "S4": session_4,
    "S5": session_5,  "S6": session_6,  "S7": session_7,  "S8": session_8,
    "S9": session_9,  "S10": session_10, "S11": session_11, "S12": session_12,
    "S13": session_13, "S14": session_14, "S15": session_15, "S16": session_16,
    "Engine":    render_chart_engine,
    "Story":     render_storytelling_builder,
    "Cases":     render_case_library,
    "Quiz":      render_quiz_zone,
    "Resources": render_resources,
}

render_fn = RENDER_MAP.get(st.session_state.page)
if render_fn:
    render_fn()
else:
    st.warning(f"Page not found: **{st.session_state.page}**")
    render_home()

footer()
