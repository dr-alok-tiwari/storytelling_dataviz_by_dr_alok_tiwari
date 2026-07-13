"""Reusable, accessible UI components for the teaching application."""

from __future__ import annotations

import re
from html import escape
from typing import Iterable

import streamlit as st

# ── Colour system ─────────────────────────────────────────────────────────────
PRIMARY = "#1B4F8A"
ACCENT = "#C77C02"  # Darker gold for accessible text/lines on light surfaces.
SUCCESS = "#16844A"
WARNING = "#B85C00"
DANGER = "#C0392B"
SOFT_BG = "#F5F7FB"
CARD_BG = "#FFFFFF"
TEXT_DARK = "#17212B"
TEXT_MUTED = "#526171"
BORDER = "#D9E2EC"

MODULE_COLORS = {
    1: "#1B4F8A",
    2: "#0F766E",
    3: "#6D3A8D",
    4: "#9F3A2F",
}

MODULE_LABELS = {
    1: "Module 1 — Foundations",
    2: "Module 2 — Dashboard Design",
    3: "Module 3 — Storytelling",
    4: "Module 4 — Business & Strategy",
}

SESSION_MODULE = {
    **{i: 1 for i in range(1, 5)},
    **{i: 2 for i in range(5, 9)},
    **{i: 3 for i in range(9, 13)},
    **{i: 4 for i in range(13, 17)},
}

SESSION_TITLES = {
    1: "Why Data Visualization and Storytelling Matter",
    2: "Mapping Data to Visual Forms",
    3: "Coordinate Systems, Axes, and Scales",
    4: "Color, Emphasis, and Visual Attention",
    5: "Visualizing Amounts with a Message",
    6: "Visualizing Distributions and Variation",
    7: "Visualizing Proportions and Composition",
    8: "Critiquing and Reframing Weak Visual Stories",
    9: "Visualizing Relationships and Building Insight",
    10: "Visualizing Time Series and Change Over Time",
    11: "Dashboard Storytelling for Business Audiences",
    12: "Annotation, Titles, Captions, and Narrative Flow",
    13: "Common Pitfalls in Data Storytelling",
    14: "Strategy Communication through Visual Stories",
    15: "Integrated Storytelling with Data Workshop",
    16: "Guest Session — Healthcare Data Visualization",
}

SESSION_CLO = {
    1: "CLO1",
    2: "CLO2",
    3: "CLO2",
    4: "CLO2",
    5: "CLO2",
    6: "CLO2",
    7: "CLO2",
    8: "CLO2",
    9: "CLO3",
    10: "CLO3",
    11: "CLO3",
    12: "CLO3",
    13: "CLO4",
    14: "CLO4",
    15: "CLO4",
    16: "CLO4",
}


# ── Backward-compatible assessment radios ─────────────────────────────────────
# The existing session modules historically pass index=0 to assessment radios.
# This narrow compatibility layer changes only known assessment widgets to a
# blank default. New code should always pass index=None explicitly.
_ORIGINAL_ST_RADIO = st.radio


def _has_numeric_suffix(value: str, prefix: str) -> bool:
    return value.startswith(prefix) and value[len(prefix) :].isdigit()


def _is_assessment_radio(label: object, key: object) -> bool:
    key_s = "" if key is None else str(key)
    label_s = "" if label is None else str(label).strip().lower()

    if key_s.startswith("quiz_"):
        return True
    if key_s in {"s1_demo_q", "s1_gap"}:
        return True

    numeric_prefixes = (
        "s2_lab_",
        "s3_scale_",
        "s4_pal_",
        "s6_dist_",
        "s7_pie_",
    )
    if any(_has_numeric_suffix(key_s, prefix) for prefix in numeric_prefixes):
        return True

    return label_s in {"select your answer", "select your answer:"}


def _assessment_radio_compat(label, options, *args, **kwargs):
    if _is_assessment_radio(label, kwargs.get("key")) and kwargs.get("index", 0) == 0:
        kwargs["index"] = None
    return _ORIGINAL_ST_RADIO(label, options, *args, **kwargs)


if getattr(st.radio, "__name__", "") != "_assessment_radio_compat":
    st.radio = _assessment_radio_compat


# ── Styling ────────────────────────────────────────────────────────────────────
def inject_css(*, classroom_mode: bool = False, reduce_motion: bool = False) -> None:
    """Inject a restrained responsive layer on top of the native Streamlit theme."""
    body_size = "1.18rem" if classroom_mode else "1.02rem"
    small_size = "0.98rem" if classroom_mode else "0.88rem"
    control_size = "1.05rem" if classroom_mode else "0.94rem"
    hero_title = "clamp(2.25rem, 3.4vw, 3.4rem)" if classroom_mode else "clamp(2rem, 3vw, 3rem)"
    motion_rule = "none !important" if reduce_motion else "background-color .15s ease, border-color .15s ease, transform .15s ease"

    st.markdown(
        f"""
        <style>
        :root {{
            --app-primary: {PRIMARY};
            --app-accent: {ACCENT};
            --app-success: {SUCCESS};
            --app-warning: {WARNING};
            --app-danger: {DANGER};
            --app-text: {TEXT_DARK};
            --app-muted: {TEXT_MUTED};
            --app-border: {BORDER};
            --app-surface: {CARD_BG};
            --app-soft: {SOFT_BG};
            --app-body-size: {body_size};
            --app-small-size: {small_size};
            --app-control-size: {control_size};
        }}

        html, body, [data-testid="stAppViewContainer"] {{
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                         "Segoe UI", sans-serif;
            color: var(--app-text);
        }}

        [data-testid="stMainBlockContainer"] {{
            max-width: 1440px;
            padding-top: 1.6rem;
            padding-bottom: 2.5rem;
        }}

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li {{
            font-size: var(--app-body-size);
            line-height: 1.66;
        }}

        h1 {{ font-size: clamp(2rem, 3vw, 3rem); letter-spacing: -0.025em; }}
        h2 {{ font-size: clamp(1.65rem, 2.4vw, 2.25rem); letter-spacing: -0.018em; }}
        h3 {{ font-size: clamp(1.3rem, 1.8vw, 1.65rem); }}
        h4 {{ font-size: clamp(1.1rem, 1.4vw, 1.3rem); }}

        .hero-strip {{
            background: linear-gradient(135deg, #123A68 0%, #1B4F8A 55%, #2563A6 100%);
            color: #FFFFFF;
            padding: clamp(1.5rem, 3vw, 2.6rem);
            border-radius: 1rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 12px 30px rgba(18, 58, 104, 0.18);
        }}
        .hero-strip h1 {{
            font-size: {hero_title};
            font-weight: 780;
            line-height: 1.08;
            margin: 0 0 .55rem;
            color: #FFFFFF;
        }}
        .hero-strip p {{
            font-size: clamp(1rem, 1.3vw, 1.2rem);
            line-height: 1.55;
            opacity: .95;
            margin: 0;
            max-width: 78rem;
        }}

        .module-header {{
            display: inline-flex;
            align-items: center;
            min-height: 2.35rem;
            padding: .55rem .95rem;
            border-radius: 999px;
            color: #FFFFFF;
            font-weight: 750;
            font-size: var(--app-small-size);
            letter-spacing: .01em;
            margin-bottom: .65rem;
        }}

        .session-title {{
            color: var(--session-color, var(--app-primary));
            margin: .15rem 0 .7rem;
            line-height: 1.18;
        }}

        .session-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: .55rem;
            align-items: center;
            margin-bottom: .8rem;
        }}
        .session-meta span {{
            background: #EEF4FA;
            border: 1px solid #D6E4F0;
            color: #29445F;
            border-radius: 999px;
            padding: .3rem .7rem;
            font-size: var(--app-small-size);
            font-weight: 650;
        }}

        .callout-insight, .callout-manager, .callout-mistake, .callout-action {{
            border-radius: .65rem;
            padding: 1rem 1.15rem;
            margin: .9rem 0;
            font-size: var(--app-body-size);
            line-height: 1.58;
            border: 1px solid transparent;
        }}
        .callout-insight {{ background: #EAF4FF; border-color: #B7D8F5; border-left: 5px solid #2563A6; }}
        .callout-manager {{ background: #EAF8F0; border-color: #B8E2CA; border-left: 5px solid {SUCCESS}; }}
        .callout-mistake {{ background: #FFF5E8; border-color: #F1D3A9; border-left: 5px solid {WARNING}; }}
        .callout-action {{ background: #FCEDEA; border-color: #EDC0B9; border-left: 5px solid {DANGER}; }}
        .callout-insight strong, .callout-manager strong,
        .callout-mistake strong, .callout-action strong {{
            display: block;
            font-size: var(--app-small-size);
            text-transform: uppercase;
            letter-spacing: .055em;
            margin-bottom: .38rem;
        }}

        .session-card, .content-card {{
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            border-radius: .8rem;
            padding: 1rem 1.15rem;
            margin-bottom: .8rem;
            box-shadow: 0 3px 10px rgba(25, 42, 62, .055);
            min-height: 100%;
        }}
        .session-card h3 {{ margin: 0 0 .3rem; font-size: 1.08rem; color: var(--app-primary); }}
        .session-card p {{ margin: 0; font-size: var(--app-small-size); color: var(--app-muted); }}

        .kpi-card {{
            background: var(--app-surface);
            border: 1px solid var(--app-border);
            border-radius: .8rem;
            padding: 1rem 1.2rem;
            text-align: center;
            box-shadow: 0 3px 10px rgba(25, 42, 62, .055);
        }}
        .kpi-value {{ font-size: clamp(1.75rem, 2.8vw, 2.4rem); font-weight: 760; color: var(--app-primary); }}
        .kpi-label {{ font-size: var(--app-small-size); color: var(--app-muted); margin-top: .2rem; }}

        .sidebar-brand {{
            display: flex;
            align-items: center;
            gap: .7rem;
            padding: .25rem 0 .8rem;
        }}
        .sidebar-brand-icon {{ font-size: 1.9rem; line-height: 1; }}
        .sidebar-brand-title {{ color: #F8FAFC; font-size: 1rem; font-weight: 760; }}
        .sidebar-brand-subtitle {{ color: #CBD5E1; font-size: .82rem; margin-top: .1rem; }}

        [data-testid="stSidebar"] {{ border-right: 1px solid rgba(255,255,255,.08); }}
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
            font-size: var(--app-small-size);
        }}

        [data-baseweb="tab-list"] {{
            gap: .35rem;
            background: #EEF3F8;
            padding: .35rem;
            border-radius: .7rem;
            overflow-x: auto;
        }}
        [data-baseweb="tab"] {{
            border-radius: .5rem;
            min-height: 2.8rem;
            font-weight: 680;
            font-size: var(--app-control-size);
            padding-inline: .85rem;
        }}

        .stButton > button,
        .stDownloadButton > button,
        [data-testid="stPageLink"] a {{
            min-height: 2.65rem;
            border-radius: .55rem;
            font-weight: 680;
            font-size: var(--app-control-size);
            transition: {motion_rule};
        }}
        .stButton > button:hover,
        .stDownloadButton > button:hover {{ transform: translateY(-1px); }}

        [data-testid="stExpander"] details summary p {{
            font-size: var(--app-control-size);
            font-weight: 680;
        }}

        [data-testid="stDataFrame"] {{
            border: 1px solid var(--app-border);
            border-radius: .65rem;
            overflow: hidden;
        }}

        .quiz-reveal {{
            background: #F0FFF4;
            border: 1px solid #9FD5B5;
            border-radius: .65rem;
            padding: 1rem;
            margin-top: .5rem;
        }}

        .app-footer {{
            text-align: center;
            color: var(--app-muted);
            font-size: max(.85rem, var(--app-small-size));
            padding: 2rem 0 1rem;
            border-top: 1px solid var(--app-border);
            margin-top: 3rem;
            line-height: 1.7;
        }}
        .app-footer a {{ color: var(--app-primary); text-decoration-thickness: .08em; }}

        @media (max-width: 900px) {{
            [data-testid="stMainBlockContainer"] {{ padding-inline: 1rem; }}
            .hero-strip {{ border-radius: .8rem; }}
        }}

        @media (max-width: 640px) {{
            [data-testid="stHorizontalBlock"] {{ gap: .75rem; }}
            .hero-strip {{ padding: 1.35rem 1.1rem; }}
            .module-header {{ border-radius: .55rem; width: 100%; }}
            .session-meta {{ gap: .35rem; }}
            .session-meta span {{ font-size: .82rem; }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                animation-duration: .01ms !important;
                animation-iteration-count: 1 !important;
                scroll-behavior: auto !important;
                transition-duration: .01ms !important;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── Shared components ──────────────────────────────────────────────────────────
def _callout(css_class: str, icon: str, label: str, body: str) -> None:
    st.markdown(
        f'<div class="{css_class}"><strong>{icon} {escape(label)}</strong>{body}</div>',
        unsafe_allow_html=True,
    )


def callout_insight(body: str, label: str = "Key Insight") -> None:
    _callout("callout-insight", "💡", label, body)


def callout_manager(body: str, label: str = "Managerial Meaning") -> None:
    _callout("callout-manager", "📊", label, body)


def callout_mistake(body: str, label: str = "Common Mistake") -> None:
    _callout("callout-mistake", "⚠️", label, body)


def callout_action(body: str, label: str = "Action Recommendation") -> None:
    _callout("callout-action", "🎯", label, body)


def hero(title: str, subtitle: str = "") -> None:
    subtitle_html = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f'<div class="hero-strip"><h1>{escape(title)}</h1>{subtitle_html}</div>',
        unsafe_allow_html=True,
    )


def _page_links(n: int) -> None:
    session_pages = st.session_state.get("_session_pages", {})
    if not session_pages:
        return

    previous_col, roadmap_col, next_col = st.columns([1, 1, 1])
    with previous_col:
        if n > 1 and n - 1 in session_pages:
            st.page_link(
                session_pages[n - 1],
                label=f"Session {n - 1}",
                icon=":material/arrow_back:",
                use_container_width=True,
            )
    with roadmap_col:
        roadmap = st.session_state.get("_roadmap_page")
        if roadmap is not None:
            st.page_link(
                roadmap,
                label="Roadmap",
                icon=":material/route:",
                use_container_width=True,
            )
    with next_col:
        if n < 16 and n + 1 in session_pages:
            st.page_link(
                session_pages[n + 1],
                label=f"Session {n + 1}",
                icon=":material/arrow_forward:",
                use_container_width=True,
            )


def session_header(n: int) -> None:
    mod = SESSION_MODULE[n]
    color = MODULE_COLORS[mod]
    clo = SESSION_CLO[n]
    completed = bool(st.session_state.get("completed", {}).get(n, False))
    status = "Completed" if completed else "In progress"
    status_icon = "✅" if completed else "○"

    st.markdown(
        f"""
        <div class="module-header" style="background:{color};">
            {escape(MODULE_LABELS[mod])} &nbsp;•&nbsp; Session {n} &nbsp;•&nbsp; {clo}
        </div>
        <h2 class="session-title" style="--session-color:{color};">
            Session {n}: {escape(SESSION_TITLES[n])}
        </h2>
        <div class="session-meta">
            <span>⏱ 75 minutes</span>
            <span>🎓 {clo}</span>
            <span>{status_icon} {status}</span>
            <span>🧪 Synthetic educational data</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _page_links(n)
    st.divider()


def _session_number_from_key(key: str) -> int | None:
    match = re.search(r"(?:refl|reflection)_s(\d+)", key)
    return int(match.group(1)) if match else None


def reflection_box(prompt: str, key: str) -> None:
    st.markdown("---")
    st.markdown("### 🪞 Reflection")
    st.markdown(f"*{prompt}*")
    st.text_area(
        "Your reflection (private to this browser session):",
        key=key,
        height=110,
        placeholder="Write the insight you want to remember or apply.",
    )

    session_number = _session_number_from_key(key)
    if session_number is None:
        return

    completed = st.session_state.setdefault("completed", {i: False for i in range(1, 17)})
    widget_key = f"session_complete_{session_number}"
    if widget_key not in st.session_state:
        st.session_state[widget_key] = bool(completed.get(session_number, False))

    done = st.toggle(
        f"Mark Session {session_number} complete",
        key=widget_key,
        help="This updates the course-progress indicator for the current browser session.",
    )
    completed[session_number] = bool(done)

    if done:
        st.success(
            f"Session {session_number} completed. Use the navigation above to continue.",
            icon="✅",
        )


def metric_cards(items: Iterable[tuple[str, str]]) -> None:
    """Render responsive KPI-style cards from (label, value) pairs."""
    items = list(items)
    if not items:
        return
    columns = st.columns(min(len(items), 4))
    for column, (label, value) in zip(columns, items):
        column.markdown(
            f'<div class="kpi-card"><div class="kpi-value">{escape(value)}</div>'
            f'<div class="kpi-label">{escape(label)}</div></div>',
            unsafe_allow_html=True,
        )


def footer() -> None:
    st.markdown(
        '<div class="app-footer">'
        "Storytelling using Data Visualization &nbsp;·&nbsp; PGDM-BDA &nbsp;·&nbsp; "
        "Goa Institute of Management, Goa<br>"
        "© 2026 Dr. Alok Tiwari &nbsp;·&nbsp; All datasets are synthetic and for educational use only."
        "</div>",
        unsafe_allow_html=True,
    )
