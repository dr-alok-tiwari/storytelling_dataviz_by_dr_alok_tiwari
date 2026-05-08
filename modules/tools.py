"""
tools.py
Special interactive tools:
- Chart Recommendation Engine
- Storytelling Framework Builder
- Dashboard Design Studio
- Business Case Library
- Quiz Zone
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

from modules.ui_components import (
    callout_insight, callout_manager, callout_mistake, callout_action,
    hero, footer, PRIMARY, ACCENT, SUCCESS, DANGER
)
from modules.data_generators import (
    retail_sales, marketing_campaign, operations_delays,
    financial_expenses, healthcare_patient_flow, bed_occupancy,
    regional_sales, scatter_sales_spend, time_series_revenue
)
from modules.quiz_bank import QUIZ_BANK

rng = np.random.default_rng(42)
WARNING = "#E67E22"


# ─────────────────────────────────────────────────────────────────────────────
#  CHART RECOMMENDATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────
CHART_RECS = {
    ("categorical", "compare", "executive"): {
        "charts": ["Horizontal sorted bar chart", "Dot plot"],
        "why": "Executives need to rank and compare quickly. Horizontal bars with category labels are easiest to read on a large screen.",
        "avoid": "3D bar charts, unsorted bars, pie charts with many slices."
    },
    ("categorical", "rank", "executive"): {
        "charts": ["Horizontal bar (sorted descending)", "Lollipop chart"],
        "why": "Rank ordering is the primary task. Sorted horizontal bars make position encoding work perfectly.",
        "avoid": "Unsorted bars, pie/donut charts."
    },
    ("numerical", "distribution", "analyst"): {
        "charts": ["Box plot", "Violin plot", "Histogram"],
        "why": "Analysts need to see median, spread, and outliers — not just averages. Box and violin plots show all of these.",
        "avoid": "Bar chart of averages (hides variance), pie charts."
    },
    ("numerical", "show relationship", "analyst"): {
        "charts": ["Scatter plot with trend line", "Bubble chart", "Correlation heat map"],
        "why": "Scatter plots are the definitive tool for showing relationships between two quantitative variables.",
        "avoid": "Line charts (for non-time data), bar charts."
    },
    ("time-series", "show trend", "executive"): {
        "charts": ["Line chart (annotated)", "Area chart (single series)"],
        "why": "Line charts encode trend in slope — the most natural reading for temporal data. Annotation adds the business narrative.",
        "avoid": "Pie charts, 3D area charts, bar charts for long time series."
    },
    ("time-series", "show trend", "analyst"): {
        "charts": ["Line chart with confidence band", "Multiple line chart (highlighted)", "Heat map calendar"],
        "why": "Analysts may need to see variance and seasonality. Heat map calendars reveal weekly/seasonal patterns invisible on line charts.",
        "avoid": "Spaghetti charts (>5 unlabeled lines), pie charts."
    },
    ("time-series", "show deviation", "executive"): {
        "charts": ["Line with reference band", "Diverging bar (vs target)"],
        "why": "Executives need to see where performance exceeds or falls short of targets — diverging from a baseline makes this immediate.",
        "avoid": "Standard bar charts that hide the deviation direction."
    },
    ("categorical", "show composition", "executive"): {
        "charts": ["100% stacked bar", "Donut chart (≤5 categories)"],
        "why": "100% stacked bar shows both absolute values and relative composition. Donut works only for very few categories.",
        "avoid": "Pie with >5 categories, 3D pie charts."
    },
    ("categorical", "show composition", "analyst"): {
        "charts": ["Treemap", "Stacked bar", "Sunburst chart"],
        "why": "Treemaps show hierarchical composition efficiently. Sunbursts add a second tier without overwhelming.",
        "avoid": "Pie with >5 slices."
    },
    ("numerical", "compare", "operations manager"): {
        "charts": ["Side-by-side bar", "Bullet chart", "Small multiples"],
        "why": "Operations managers need to benchmark departments/shifts. Side-by-side bars and bullet charts show actuals vs targets clearly.",
        "avoid": "Pie charts, single-series charts that hide variation."
    },
    ("relational", "show relationship", "analyst"): {
        "charts": ["Network graph", "Chord diagram", "Sankey diagram"],
        "why": "Relational data (flows, connections) needs purpose-built charts. Sankey charts show flows through stages perfectly.",
        "avoid": "Bar or line charts — they cannot encode network structure."
    },
    ("geospatial", "compare", "executive"): {
        "charts": ["Choropleth map (shaded regions)", "Bubble map (sized markers)"],
        "why": "Geographic patterns are best revealed with maps. Choropleth works for regional aggregates; bubble maps for point data.",
        "avoid": "Bar charts for geographic data — miss the spatial pattern."
    },
    ("hierarchical", "show composition", "analyst"): {
        "charts": ["Treemap", "Sunburst chart", "Icicle chart"],
        "why": "Hierarchical data has two levels of grouping. Treemaps encode size as area — the natural mental model for hierarchy.",
        "avoid": "Pie charts — they cannot show hierarchy."
    },
    ("numerical", "show distribution", "healthcare manager"): {
        "charts": ["Box plot", "Histogram", "Violin plot with box"],
        "why": "Clinical decisions depend on understanding the full distribution of outcomes, not just averages.",
        "avoid": "KPI cards alone — they hide the variance that drives clinical decisions."
    },
    ("time-series", "compare", "healthcare manager"): {
        "charts": ["Control chart (SPC)", "Multi-line annotated chart"],
        "why": "Healthcare managers need to distinguish normal variation from signals requiring intervention. SPC charts are the standard tool.",
        "avoid": "Plain line charts without control limits — they make all variation look significant."
    },
}


def get_recommendation(data_type, question, audience):
    key = (data_type, question, audience)
    if key in CHART_RECS:
        return CHART_RECS[key]
    # Fallback
    return {
        "charts": ["Bar chart (sorted)", "Line chart (for time data)", "Scatter plot (for relationships)"],
        "why": "This combination is common in business settings. Start with the simplest chart that answers the question.",
        "avoid": "3D charts, pie charts with many segments, rainbow color palettes."
    }


def render_chart_engine():
    hero("📊 Chart Selection Engine",
         "Select your data type, business question, and audience — get a tailored chart recommendation.")
    col1, col2, col3 = st.columns(3)
    data_type = col1.selectbox("Data type:", [
        "categorical", "numerical", "time-series", "geospatial", "relational", "hierarchical"
    ], key="ce_dtype")
    question = col2.selectbox("Business question:", [
        "compare", "rank", "show trend", "show distribution", "show relationship",
        "show composition", "show deviation"
    ], key="ce_q")
    audience = col3.selectbox("Audience:", [
        "executive", "analyst", "operations manager", "healthcare manager", "customer"
    ], key="ce_aud")

    if st.button("Get Recommendation ▶", key="ce_rec"):
        rec = get_recommendation(data_type, question, audience)
        st.markdown("---")
        st.markdown("### ✅ Recommended Chart Types")
        for i, chart in enumerate(rec["charts"], 1):
            st.markdown(f"**{i}. {chart}**")
        callout_insight(rec["why"], "Why These Charts?")
        callout_mistake(rec["avoid"], "Avoid")

        st.markdown("### 📌 Live Example")
        if data_type in ("categorical", "hierarchical") and question in ("compare", "rank", "show composition"):
            df = regional_sales().groupby("region")["sales"].sum().reset_index().sort_values("sales", ascending=False)
            if "composition" in question:
                fig = px.pie(df, names="region", values="sales", title=f"Example: {rec['charts'][0]}")
            else:
                fig = go.Figure(go.Bar(x=df["region"], y=df["sales"], marker_color=PRIMARY))
                fig.update_layout(title=f"Example: {rec['charts'][0]}")
        elif data_type == "time-series":
            df = time_series_revenue()
            fig = go.Figure(go.Scatter(x=df["month"], y=df["revenue"], mode="lines",
                                        line=dict(color=PRIMARY, width=2.5)))
            fig.update_layout(title=f"Example: {rec['charts'][0]}")
        elif question == "show relationship":
            df = scatter_sales_spend()
            fig = px.scatter(df, x="marketing_spend", y="revenue", color="channel", trendline="ols",
                             title=f"Example: {rec['charts'][0]}")
        elif question == "show distribution":
            from modules.data_generators import customer_satisfaction
            df = customer_satisfaction()
            fig = px.box(df, x="department", y="nps_score", color="department",
                         title=f"Example: {rec['charts'][0]}")
        else:
            df = financial_expenses().groupby("category")["amount_lakhs"].sum().reset_index()
            fig = px.bar(df.sort_values("amount_lakhs", ascending=False),
                         x="category", y="amount_lakhs",
                         title=f"Example: {rec['charts'][0]}",
                         color_discrete_sequence=[PRIMARY])
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
#  STORYTELLING FRAMEWORK BUILDER
# ─────────────────────────────────────────────────────────────────────────────
def render_storytelling_builder():
    hero("📝 Storytelling Framework Builder",
         "Structure your data story using the proven Context → Insight → Recommendation framework.")
    st.write("""
    Complete each layer of the storytelling framework below.
    The app will assemble your story and let you download it.
    """)
    st.markdown("---")

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("#### 1. Context — What is the situation?")
        domain = st.selectbox("Business domain:", [
            "Sales", "Marketing", "Operations", "Finance", "Healthcare", "HR", "Strategy"
        ], key="sb_domain")
        period = st.text_input("Time period:", "Q3 2024", key="sb_period")
        context_text = st.text_area("Describe the situation in 2–3 sentences:", height=70,
                                     placeholder="e.g., Revenue has been declining for 3 consecutive quarters across the North and West regions.",
                                     key="sb_context")

        st.markdown("#### 2. Business Question — What are you trying to answer?")
        biz_q = st.text_input("Business question:", key="sb_q",
                               placeholder="e.g., Which region is underperforming and why?")

        st.markdown("#### 3. Data Evidence — What does the data show?")
        data_point_1 = st.text_input("Key finding 1:", key="sb_dp1",
                                      placeholder="e.g., North region is 34% below Q3 target")
        data_point_2 = st.text_input("Key finding 2:", key="sb_dp2",
                                      placeholder="e.g., Marketing spend in North is 22% lower than other regions")
        data_point_3 = st.text_input("Key finding 3 (optional):", key="sb_dp3")

        st.markdown("#### 4. Pattern — What pattern do you observe?")
        pattern = st.text_area("Describe the pattern:", height=60, key="sb_pattern",
                                placeholder="e.g., Underperforming regions correlate with lower marketing spend and fewer sales visits.")

        st.markdown("#### 5. Insight — What does this mean?")
        insight = st.text_area("State the insight:", height=60, key="sb_insight",
                                placeholder="e.g., The North's underperformance is driven by resource deficit, not market conditions.")

        st.markdown("#### 6. Implication — So what?")
        implication = st.text_area("Business implication:", height=60, key="sb_impl",
                                    placeholder="e.g., Without intervention, the North will miss annual target by ₹40L.")

        st.markdown("#### 7. Recommendation — What should be done?")
        rec = st.text_area("Your recommendation:", height=70, key="sb_rec",
                            placeholder="e.g., Reallocate ₹8L from South marketing budget to North in Q4. Target 15% recovery.")

        st.markdown("#### 8. Action — Who does what, by when?")
        action = st.text_input("Specific action:", key="sb_action",
                                placeholder="e.g., Regional VP to submit revised plan by Oct 15.")

    with col2:
        st.markdown("#### 📋 Your Story Preview")
        story_parts = [
            ("Context", context_text, "📌"),
            ("Question", biz_q, "❓"),
            ("Evidence", f"• {data_point_1}\n• {data_point_2}\n{'• ' + data_point_3 if data_point_3 else ''}", "📊"),
            ("Pattern", pattern, "🔍"),
            ("Insight", insight, "💡"),
            ("Implication", implication, "⚡"),
            ("Recommendation", rec, "🎯"),
            ("Action", action, "✅"),
        ]
        for label, content, icon in story_parts:
            if content.strip():
                st.markdown(f"**{icon} {label}**")
                st.markdown(f"> {content}")
            else:
                st.markdown(f"**{icon} {label}** — *not yet filled*")

        if st.button("Generate & Download Story", key="sb_dl"):
            story_text = f"""DATA STORY: {domain} | {period}
{'='*50}

CONTEXT
{context_text}

BUSINESS QUESTION
{biz_q}

DATA EVIDENCE
• {data_point_1}
• {data_point_2}
{"• " + data_point_3 if data_point_3 else ""}

PATTERN
{pattern}

INSIGHT
{insight}

IMPLICATION
{implication}

RECOMMENDATION
{rec}

ACTION
{action}

---
Generated by: Storytelling using Data Visualization App
PGDM-BDA | Goa Institute of Management | Dr. Alok Tiwari
"""
            st.download_button("⬇ Download Story (.txt)", story_text.encode(),
                               f"data_story_{domain.lower()}.txt", "text/plain")
            callout_action("Story assembled. Check: does each section logically lead to the next? Is the recommendation specific enough to act on?", "Story Check")


# ─────────────────────────────────────────────────────────────────────────────
#  BUSINESS CASE LIBRARY
# ─────────────────────────────────────────────────────────────────────────────
CASES = {
    "Sales Performance Story": {
        "dataset": "regional_sales",
        "context": "A regional FMCG company is preparing its Q3 business review. The sales director suspects North region is underperforming but needs data to make the case for resource reallocation.",
        "questions": [
            "Which region has the largest gap between actual sales and target?",
            "Which product category drives the most variance across regions?",
            "If you could reallocate budget from one region to another, what would you recommend and why?"
        ],
        "story_title": "North and West Regions Need Immediate Support — ₹15L Reallocation Recommended"
    },
    "Marketing Campaign ROI Story": {
        "dataset": "marketing_campaign",
        "context": "The CMO is reviewing marketing channel performance before finalizing next year's budget. Total marketing budget is ₹150L. The question: which channels should be scaled, and which should be cut?",
        "questions": [
            "Which channel has the highest ROI?",
            "Which channel spends the most but delivers the least per rupee?",
            "If budget must be cut by 20%, which channel would you cut first, and why?"
        ],
        "story_title": "SEO and Email Deliver 3× More Return Per Rupee — Double Down There, Cut TV"
    },
    "Operations Delay Story": {
        "dataset": "operations_delays",
        "context": "The operations head is concerned about increasing delivery delays. Customer complaints have risen 28% this quarter. The board wants a plan by end of month.",
        "questions": [
            "Is the delay trend improving or worsening over time?",
            "Is there a relationship between shipment volume and delay hours?",
            "What level of on-time delivery is realistic as a 6-month target?"
        ],
        "story_title": "Delays Are Improving But Still Above Target — Process Review Required in Weeks 12–20"
    },
    "Finance Cost Control Story": {
        "dataset": "financial_expenses",
        "context": "The CFO wants to understand cost structure before presenting to the board. Total costs have grown 18% over 8 quarters. The board wants to see which categories are driving this growth.",
        "questions": [
            "Which cost category has grown fastest as a proportion of total cost?",
            "Are any categories shrinking as a share of total?",
            "What single cost action would have the highest impact on profitability?"
        ],
        "story_title": "Technology Cost Growing 3× Faster Than Revenue — Vendor Contract Review Urgent"
    },
    "Healthcare Hospital Dashboard Story": {
        "dataset": "bed_occupancy",
        "context": "The hospital administrator is preparing the monthly operations review. Three wards have been flagged as potential capacity risks. The clinical director needs to decide whether to open overflow capacity.",
        "questions": [
            "Which ward is most consistently above 85% occupancy?",
            "Are there specific days of week when occupancy spikes?",
            "Should overflow capacity be opened? What data supports that decision?"
        ],
        "story_title": "ICU and General Wards Routinely Exceed Safe Threshold — Overflow Capacity Recommended"
    },
    "Strategy Market Entry Story": {
        "dataset": "scatter_sales_spend",
        "context": "A retail brand is evaluating entry into two new channels (Online and Both). Historical data from existing channels shows the relationship between spend and revenue returns.",
        "questions": [
            "Which existing channel shows the strongest spend-revenue relationship?",
            "Are there channels where spend is high but returns are low?",
            "Based on the pattern, which new channel entry would you recommend and what initial budget?"
        ],
        "story_title": "Online Channel ROI Is 2.4× Offline — Prioritise Digital-First Market Entry"
    },
}

DATASET_LOADERS = {
    "regional_sales": regional_sales,
    "marketing_campaign": marketing_campaign,
    "operations_delays": operations_delays,
    "financial_expenses": financial_expenses,
    "bed_occupancy": bed_occupancy,
    "scatter_sales_spend": scatter_sales_spend,
}


def render_case_library():
    hero("📚 Business Case Library",
         "Six guided case studies for sales, marketing, operations, finance, healthcare, and strategy.")
    case_name = st.selectbox("Select case:", list(CASES.keys()), key="cl_case")
    case = CASES[case_name]
    df = DATASET_LOADERS[case["dataset"]]()
    st.markdown("---")
    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown(f"### 📌 Business Context")
        st.write(case["context"])
        st.markdown(f"**Story headline:** *{case['story_title']}*")
        st.markdown("#### 🔍 Guided Questions")
        for i, q in enumerate(case["questions"], 1):
            st.markdown(f"{i}. {q}")
            st.text_input(f"Your answer {i}:", key=f"cl_ans_{case_name}_{i}")
    with col2:
        st.markdown("#### 📊 Dataset Preview")
        st.dataframe(df.head(20), use_container_width=True, height=220)
        st.download_button("⬇ Download Dataset", df.to_csv(index=False).encode(),
                           f"{case['dataset']}.csv", "text/csv")

    st.markdown("---")
    st.markdown("#### 📈 Guided Visualization")
    if case["dataset"] == "regional_sales":
        col_a, col_b = st.columns(2)
        with col_a:
            by_r = df.groupby("region")[["sales","target"]].sum().reset_index()
            by_r["gap"] = by_r["sales"] - by_r["target"]
            fig = px.bar(by_r.sort_values("gap"), x="region", y="gap",
                         title="Sales vs Target Gap by Region",
                         color="gap", color_continuous_scale="RdYlGn")
            fig.add_hline(y=0, line_color="black")
            fig.update_layout(height=280)
            col_a.plotly_chart(fig, use_container_width=True)
        with col_b:
            fig2 = px.imshow(df.pivot_table(index="category",columns="region",values="sales"),
                             color_continuous_scale="Blues", title="Sales Heat Map",
                             aspect="auto")
            fig2.update_layout(height=280)
            col_b.plotly_chart(fig2, use_container_width=True)
    elif case["dataset"] == "marketing_campaign":
        col_a, col_b = st.columns(2)
        with col_a:
            fig = px.bar(df.sort_values("roi", ascending=False), x="channel", y="roi",
                         title="ROI by Channel (%)", color_discrete_sequence=[PRIMARY])
            fig.update_layout(height=280)
            col_a.plotly_chart(fig, use_container_width=True)
        with col_b:
            fig2 = px.scatter(df, x="spend_lakhs", y="revenue_lakhs", size="conversions",
                               color="channel", title="Spend vs Revenue (bubble = conversions)")
            fig2.update_layout(height=280)
            col_b.plotly_chart(fig2, use_container_width=True)
    elif case["dataset"] == "operations_delays":
        fig = px.line(df, x="week", y="avg_delay_hrs",
                      title="Delivery Delay Trend — Is It Improving?",
                      color_discrete_sequence=[PRIMARY])
        fig.add_hline(y=3, line_dash="dot", line_color=SUCCESS, annotation_text="Target: 3h")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    elif case["dataset"] == "financial_expenses":
        fig = px.bar(df, x="quarter", y="amount_lakhs", color="category",
                     barnorm="percent", title="Cost Mix Over Time (100% Stacked)")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    elif case["dataset"] == "bed_occupancy":
        avg_occ = df.groupby(["ward"])["occupancy_pct"].mean().reset_index()
        fig = go.Figure(go.Bar(x=avg_occ["occupancy_pct"], y=avg_occ["ward"], orientation="h",
                                marker_color=[DANGER if v > 85 else ACCENT if v > 75 else PRIMARY
                                               for v in avg_occ["occupancy_pct"]]))
        fig.add_vline(x=85, line_dash="dot", line_color=DANGER, annotation_text="Alert: 85%")
        fig.update_layout(title="Average Ward Occupancy", height=300, xaxis_title="Occupancy (%)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.scatter(df, x="marketing_spend", y="revenue", color="channel",
                         trendline="ols", title="Spend vs Revenue by Channel")
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("💡 Reveal Recommended Visual Story & Managerial Recommendation"):
        callout_action(f"**Headline:** {case['story_title']}\n\nBuild 3 charts: context (overview), evidence (key pattern), recommendation (what to do). Keep the story to one slide per chart.", "Recommended Approach")


# ─────────────────────────────────────────────────────────────────────────────
#  FULL QUIZ ZONE
# ─────────────────────────────────────────────────────────────────────────────
def render_quiz_zone():
    hero("❓ Quiz Zone", "50+ questions across all 16 sessions. Test your data storytelling knowledge.")
    filter_session = st.selectbox("Filter by session:", ["All"] + [str(i) for i in range(1, 17)], key="qz_sess")
    filter_type = st.selectbox("Filter by type:", ["All", "MCQ", "TrueFalse", "Scenario"], key="qz_type")

    qs = QUIZ_BANK
    if filter_session != "All":
        qs = [q for q in qs if q["session"] == int(filter_session)]
    if filter_type != "All":
        qs = [q for q in qs if q["type"] == filter_type]

    st.info(f"Showing {len(qs)} questions.")
    for i, q in enumerate(qs):
        with st.expander(f"Q{i+1} | Session {q['session']} | {q['clo']} | {q['type']} — {q['q'][:60]}..."):
            st.markdown(f"**{q['q']}**")
            choice = st.radio("", q["options"], key=f"qz_q{i}", index=0)
            if st.button("Reveal Answer", key=f"qz_ans{i}"):
                if choice == q["answer"]:
                    st.success(f"✅ Correct!\n\n{q['explanation']}")
                else:
                    st.error(f"❌ Correct answer: **{q['answer']}**\n\n{q['explanation']}")


# ─────────────────────────────────────────────────────────────────────────────
#  RESOURCES PAGE
# ─────────────────────────────────────────────────────────────────────────────
def render_resources():
    hero("🛠 Free Visualization Tools", "No paid software required for this course.")
    tools = [
        {
            "name": "Tableau Public",
            "url": "https://public.tableau.com",
            "desc": "Industry-leading drag-and-drop visualization. Free for public dashboards. Excellent for practice.",
            "best_for": "Interactive dashboards, maps, complex layouts",
            "effort": "Medium learning curve"
        },
        {
            "name": "Flourish",
            "url": "https://flourish.studio",
            "desc": "Browser-based, no-code. Templates for bar chart races, story maps, and scrollytelling.",
            "best_for": "Animated charts, storytelling, quick prototypes",
            "effort": "Very easy — no coding"
        },
        {
            "name": "Datawrapper",
            "url": "https://www.datawrapper.de",
            "desc": "Used by newsrooms. Excellent for clean, publication-ready charts with minimal configuration.",
            "best_for": "Line, bar, map charts for publication",
            "effort": "Very easy — upload CSV and select template"
        },
        {
            "name": "RAWGraphs",
            "url": "https://rawgraphs.io",
            "desc": "Open source. Specialises in unusual chart types: alluvial, bump, streamgraph, parallel coordinates.",
            "best_for": "Exploring chart types beyond the standard set",
            "effort": "Easy — drag and drop"
        },
        {
            "name": "Google Sheets / Excel",
            "url": "https://sheets.google.com",
            "desc": "Familiar tools with powerful charting. Good for quick exploration and presentations.",
            "best_for": "Quick charts embedded in reports and slide decks",
            "effort": "Minimal — most students already know these"
        },
        {
            "name": "Power BI Desktop",
            "url": "https://powerbi.microsoft.com/desktop",
            "desc": "Microsoft's free desktop BI tool. Excellent for business dashboards connected to data sources.",
            "best_for": "Business dashboards, reports with multiple data sources",
            "effort": "Medium — requires some setup"
        },
    ]
    cols = st.columns(2)
    for i, tool in enumerate(tools):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background:white;border:1px solid #E2EAF4;border-radius:10px;padding:1rem 1.2rem;margin-bottom:1rem;border-left:4px solid #1B4F8A;">
            <h4 style="margin:0 0 0.3rem 0;color:#1B4F8A;">{tool['name']}</h4>
            <p style="font-size:0.88rem;color:#4B5563;margin:0 0 0.4rem 0;">{tool['desc']}</p>
            <p style="font-size:0.82rem;margin:0;"><strong>Best for:</strong> {tool['best_for']}</p>
            <p style="font-size:0.82rem;margin:0.2rem 0 0 0;"><strong>Effort:</strong> {tool['effort']}</p>
            <a href="{tool['url']}" target="_blank" style="font-size:0.82rem;color:#2563EB;">→ Open tool</a>
            </div>
            """, unsafe_allow_html=True)
    callout_insight("You do not need all of these tools. Pick one (recommend Flourish or Datawrapper for beginners, Tableau for advanced) and get proficient. Depth beats breadth.", "Tool Strategy")
