"""
ui_components.py
Reusable UI components, CSS injection, and callout boxes.
"""
import streamlit as st

# ── Colour palette ────────────────────────────────────────────────────────────
PRIMARY   = "#1B4F8A"   # GIM deep blue
ACCENT    = "#F4A900"   # Gold
SUCCESS   = "#27AE60"
WARNING   = "#E67E22"
DANGER    = "#E74C3C"
SOFT_BG   = "#F4F7FC"
CARD_BG   = "#FFFFFF"
TEXT_DARK = "#1C2833"

MODULE_COLORS = {
    1: "#1B4F8A",
    2: "#117A65",
    3: "#7D3C98",
    4: "#B03A2E",
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
    1:  "Why Data Visualization and Storytelling Matter",
    2:  "Mapping Data to Visual Forms",
    3:  "Coordinate Systems, Axes, and Scales",
    4:  "Color, Emphasis, and Visual Attention",
    5:  "Visualizing Amounts with a Message",
    6:  "Visualizing Distributions and Variation",
    7:  "Visualizing Proportions and Composition",
    8:  "Critiquing and Reframing Weak Visual Stories",
    9:  "Visualizing Relationships and Building Insight",
    10: "Visualizing Time Series and Change Over Time",
    11: "Dashboard Storytelling for Business Audiences",
    12: "Annotation, Titles, Captions, and Narrative Flow",
    13: "Common Pitfalls in Data Storytelling",
    14: "Strategy Communication through Visual Stories",
    15: "Integrated Storytelling with Data Workshop",
    16: "Guest Session — Healthcare Data Visualization",
}

SESSION_CLO = {
    1: "CLO1", 2: "CLO2", 3: "CLO2", 4: "CLO2",
    5: "CLO2", 6: "CLO2", 7: "CLO2", 8: "CLO2",
    9: "CLO3", 10: "CLO3", 11: "CLO3", 12: "CLO3",
    13: "CLO4", 14: "CLO4", 15: "CLO4", 16: "CLO4",
}


def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {TEXT_DARK};
    }}

    .hero-strip {{
        background: linear-gradient(135deg, {PRIMARY} 0%, #2563EB 100%);
        color: white;
        padding: 2.4rem 2rem 2rem 2rem;
        border-radius: 14px;
        margin-bottom: 1.6rem;
    }}
    .hero-strip h1 {{
        font-family: 'Playfair Display', serif;
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0 0 0.3rem 0;
        color: white;
    }}
    .hero-strip p {{
        font-size: 1.05rem;
        opacity: 0.9;
        margin: 0;
    }}

    .module-header {{
        padding: 0.7rem 1.2rem;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.6rem;
    }}

    .session-card {{
        background: {CARD_BG};
        border: 1px solid #E2EAF4;
        border-left: 5px solid {PRIMARY};
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }}
    .session-card h3 {{ margin: 0 0 0.25rem 0; font-size: 1.05rem; font-weight: 600; color: {PRIMARY}; }}
    .session-card p  {{ margin: 0; font-size: 0.88rem; color: #5A6A7A; }}

    .callout-insight {{
        background: #EAF4FF; border-left: 5px solid #2563EB;
        border-radius: 6px; padding: 0.9rem 1.1rem; margin: 0.8rem 0; font-size: 0.93rem;
    }}
    .callout-manager {{
        background: #EAFAF1; border-left: 5px solid {SUCCESS};
        border-radius: 6px; padding: 0.9rem 1.1rem; margin: 0.8rem 0; font-size: 0.93rem;
    }}
    .callout-mistake {{
        background: #FEF9E7; border-left: 5px solid {ACCENT};
        border-radius: 6px; padding: 0.9rem 1.1rem; margin: 0.8rem 0; font-size: 0.93rem;
    }}
    .callout-action {{
        background: #FDEDEC; border-left: 5px solid {DANGER};
        border-radius: 6px; padding: 0.9rem 1.1rem; margin: 0.8rem 0; font-size: 0.93rem;
    }}
    .callout-insight strong, .callout-manager strong,
    .callout-mistake strong, .callout-action strong {{
        display: block; font-size: 0.78rem; text-transform: uppercase;
        letter-spacing: 0.05em; margin-bottom: 0.3rem; opacity: 0.7;
    }}

    .kpi-card {{
        background: {CARD_BG}; border: 1px solid #E2EAF4;
        border-radius: 10px; padding: 1rem 1.2rem; text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }}
    .kpi-value {{ font-size: 2rem; font-weight: 700; color: {PRIMARY}; line-height: 1.1; }}
    .kpi-label {{ font-size: 0.82rem; color: #6B7280; margin-top: 0.2rem; }}

    /* Quiz reveal styling */
    .quiz-reveal {{
        background: #F0FFF4; border: 1px solid #27AE60;
        border-radius: 8px; padding: 1rem; margin-top: 0.5rem;
    }}

    section[data-testid="stSidebar"] {{ background: #0D2137; }}
    section[data-testid="stSidebar"] * {{ color: #CBD5E1 !important; }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.4rem; background: #F1F5F9; padding: 0.4rem; border-radius: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{ border-radius: 6px; font-weight: 500; font-size: 0.88rem; }}

    .stButton > button {{ border-radius: 6px; font-weight: 600; font-size: 0.88rem; }}

    .streamlit-expanderHeader {{ font-weight: 600; font-size: 0.92rem; color: {PRIMARY}; }}

    hr {{ border-color: #E2EAF4; }}

    .app-footer {{
        text-align: center;
        color: #6B7280;
        font-size: 0.80rem;
        padding: 2rem 0 1rem 0;
        border-top: 2px solid #E2EAF4;
        margin-top: 3rem;
        line-height: 1.7;
    }}
    .app-footer a {{ color: #1B4F8A; text-decoration: none; }}
    </style>
    """, unsafe_allow_html=True)


# ── Callout helpers ────────────────────────────────────────────────────────────

def callout_insight(body: str, label: str = "Key Insight"):
    st.markdown(f'<div class="callout-insight"><strong>💡 {label}</strong>{body}</div>',
                unsafe_allow_html=True)

def callout_manager(body: str, label: str = "Managerial Meaning"):
    st.markdown(f'<div class="callout-manager"><strong>📊 {label}</strong>{body}</div>',
                unsafe_allow_html=True)

def callout_mistake(body: str, label: str = "Common Mistake"):
    st.markdown(f'<div class="callout-mistake"><strong>⚠️ {label}</strong>{body}</div>',
                unsafe_allow_html=True)

def callout_action(body: str, label: str = "Action Recommendation"):
    st.markdown(f'<div class="callout-action"><strong>🎯 {label}</strong>{body}</div>',
                unsafe_allow_html=True)

def hero(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="hero-strip">
        <h1>{title}</h1>
        {"<p>" + subtitle + "</p>" if subtitle else ""}
    </div>""", unsafe_allow_html=True)

def session_header(n: int):
    mod = SESSION_MODULE[n]
    color = MODULE_COLORS[mod]
    clo = SESSION_CLO[n]
    st.markdown(f"""
    <div class="module-header" style="background:{color};">
        {MODULE_LABELS[mod]}  •  Session {n}  •  {clo}
    </div>
    <h2 style="color:{color};margin-top:0.2rem;">
        Session {n}: {SESSION_TITLES[n]}
    </h2>
    """, unsafe_allow_html=True)

def reflection_box(prompt: str, key: str):
    st.markdown("---")
    st.markdown("### 🪞 Reflection")
    st.markdown(f"*{prompt}*")
    st.text_area("Your reflection (not submitted — for personal note-taking):", key=key, height=80)

def footer():
    st.markdown(
        '<div class="app-footer">'
        'Storytelling using Data Visualization &nbsp;·&nbsp; PGDM-BDA &nbsp;·&nbsp; '
        'Goa Institute of Management, Panaji, Goa<br>'
        '© 2025 Dr. Alok Tiwari. All rights reserved.'
        '</div>',
        unsafe_allow_html=True
    )
