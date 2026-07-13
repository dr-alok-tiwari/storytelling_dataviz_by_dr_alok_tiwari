"""Interactive practice tools for chart selection, storytelling, cases, and quizzes."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from modules.data_generators import (
    bed_occupancy,
    customer_satisfaction,
    financial_expenses,
    healthcare_patient_flow,
    marketing_campaign,
    operations_delays,
    regional_sales,
    scatter_sales_spend,
    time_series_revenue,
)
from modules.quiz_bank import QUIZ_BANK
from modules.ui_components import (
    ACCENT,
    DANGER,
    PRIMARY,
    SUCCESS,
    WARNING,
    callout_action,
    callout_insight,
    callout_manager,
    callout_mistake,
    hero,
)


@dataclass(frozen=True)
class ChartRecommendation:
    primary: str
    alternatives: tuple[str, ...]
    rationale: str
    avoid: str


def _audience_note(audience: str) -> str:
    notes = {
        "Executive": "Keep the visual sparse, lead with the conclusion, and label the decision-relevant value directly.",
        "Analyst": "Retain distribution, uncertainty, and diagnostic detail so the pattern can be challenged and verified.",
        "Operations manager": "Emphasise targets, exceptions, thresholds, and the owner of the next action.",
        "Healthcare manager": "Show denominators, thresholds, uncertainty, and operational context; avoid patient-identifiable detail.",
        "Customer / public": "Use plain language, direct labels, and a short explanation of what the chart does and does not prove.",
    }
    return notes[audience]


def get_recommendation(
    data_type: str,
    question: str,
    audience: str,
    category_count: int = 5,
) -> ChartRecommendation:
    """Return a deterministic recommendation for every valid input combination."""
    data_type = data_type.lower()
    question = question.lower()

    if data_type == "time series":
        if question in {"show trend", "compare", "show deviation"}:
            primary = "Annotated line chart" if question != "show deviation" else "Line chart with target band"
            alternatives = ("Small-multiple line charts", "Slope chart for two time points")
            rationale = "Time is ordered. Position and slope reveal direction, turning points, seasonality, and deviation from target."
            avoid = "Avoid pie charts and equally spaced labels for irregular time intervals."
        else:
            primary = "Calendar or period heat map"
            alternatives = ("Distribution by period", "Faceted line chart")
            rationale = "A heat map can reveal recurring temporal patterns when the question is about concentration or variation."
            avoid = "Avoid connecting observations when the time series has missing intervals."

    elif data_type == "categorical":
        if question in {"compare", "rank"}:
            primary = "Sorted horizontal bar chart"
            alternatives = ("Dot plot", "Lollipop chart")
            rationale = "A common baseline makes categorical amounts easy to compare; sorting removes mental ranking work."
            avoid = "Avoid unsorted bars, 3D effects, and pie charts when exact comparison matters."
        elif question == "show composition":
            if category_count <= 5:
                primary = "100% stacked bar chart"
                alternatives = ("Donut chart for a single total", "Treemap for hierarchy")
            else:
                primary = "Sorted bar chart of shares"
                alternatives = ("Treemap", "100% stacked bar after grouping small categories")
            rationale = "Composition requires a visible whole. A common 0–100% scale supports comparison across groups."
            avoid = "Avoid pies or donuts with more than five slices."
        elif question == "show deviation":
            primary = "Diverging bar chart"
            alternatives = ("Bullet chart", "Variance dot plot")
            rationale = "A shared zero or target baseline makes above-versus-below performance immediately visible."
            avoid = "Avoid separate charts with inconsistent scales for actual and target."
        else:
            primary = "Grouped or faceted bar chart"
            alternatives = ("Heat map", "Dot plot")
            rationale = "Categorical structure is best preserved with aligned positions rather than angle or area comparisons."
            avoid = "Avoid line charts unless the categories have a true ordered sequence."

    elif data_type == "numerical":
        if question in {"show distribution", "compare"}:
            primary = "Box plot with visible observations"
            alternatives = ("Histogram", "Violin plot")
            rationale = "Distribution charts reveal median, spread, skew, and outliers that averages conceal."
            avoid = "Avoid a bar chart of means without sample size or variation."
        elif question == "show relationship":
            primary = "Scatter plot with trend line"
            alternatives = ("Hexbin plot for dense data", "Bubble chart for a justified third variable")
            rationale = "Two position channels provide the most accurate view of association, clusters, and outliers."
            avoid = "Do not claim causation from a visual association alone."
        elif question == "show deviation":
            primary = "Distribution with reference line"
            alternatives = ("Control chart", "Diverging dot plot")
            rationale = "A reference line preserves individual variation while showing distance from a standard."
            avoid = "Avoid hiding variance inside a single KPI card."
        else:
            primary = "Histogram"
            alternatives = ("ECDF", "Density plot")
            rationale = "Numerical data should first be inspected for shape, range, gaps, and extreme observations."
            avoid = "Avoid converting continuous measurements into arbitrary categories too early."

    elif data_type == "geospatial":
        primary = "Choropleth map" if question in {"compare", "show deviation"} else "Proportional-symbol map"
        alternatives = ("Ranked bar chart alongside the map", "Small-multiple regional maps")
        rationale = "Location is part of the analytical question, so spatial adjacency and regional concentration must remain visible."
        avoid = "Avoid maps when geography is incidental; a sorted bar chart is usually more precise."

    elif data_type == "relational":
        if question in {"show relationship", "show composition"}:
            primary = "Sankey diagram"
            alternatives = ("Network graph", "Chord diagram")
            rationale = "Relational charts preserve links or flows between entities instead of flattening them into categories."
            avoid = "Avoid Sankey diagrams with too many crossing flows or unlabeled nodes."
        else:
            primary = "Adjacency matrix"
            alternatives = ("Network graph", "Ranked node table")
            rationale = "An adjacency matrix scales better than a node-link diagram when the network is dense."
            avoid = "Avoid decorative network layouts that obscure rather than explain structure."

    else:  # hierarchical
        primary = "Treemap" if question == "show composition" else "Sunburst chart"
        alternatives = ("Indented bar chart", "Icicle chart")
        rationale = "Hierarchy requires both parent–child structure and magnitude to remain visible."
        avoid = "Avoid a flat pie chart because it cannot communicate multiple levels."

    return ChartRecommendation(
        primary=primary,
        alternatives=alternatives,
        rationale=f"{rationale} {_audience_note(audience)}",
        avoid=avoid,
    )


def _example_figure(
    recommendation: ChartRecommendation,
    data_type: str,
    question: str,
) -> go.Figure:
    primary = recommendation.primary

    if primary == "Sorted horizontal bar chart":
        df = regional_sales().groupby("region", as_index=False)["sales"].sum().sort_values("sales")
        fig = px.bar(df, x="sales", y="region", orientation="h", text_auto=True)
        fig.update_traces(marker_color=PRIMARY)
        fig.update_layout(title="Regional sales ranked from lowest to highest", xaxis_title="Sales (₹ lakh)")

    elif primary == "100% stacked bar chart":
        df = financial_expenses()
        fig = px.bar(df, x="quarter", y="amount_lakhs", color="category", barnorm="percent")
        fig.update_layout(title="Cost mix across quarters", yaxis_title="Share of quarterly cost (%)")

    elif primary == "Sorted bar chart of shares":
        df = financial_expenses().groupby("category", as_index=False)["amount_lakhs"].sum()
        df["share"] = df["amount_lakhs"] / df["amount_lakhs"].sum() * 100
        df = df.sort_values("share")
        fig = px.bar(df, x="share", y="category", orientation="h", text_auto=".1f")
        fig.update_traces(marker_color=PRIMARY)
        fig.update_layout(title="Share of total cost by category", xaxis_title="Share (%)")

    elif primary in {"Diverging bar chart", "Bullet chart"}:
        df = regional_sales().groupby("region", as_index=False)[["sales", "target"]].sum()
        df["gap"] = df["sales"] - df["target"]
        df = df.sort_values("gap")
        colors = [DANGER if value < 0 else SUCCESS for value in df["gap"]]
        fig = go.Figure(go.Bar(x=df["gap"], y=df["region"], orientation="h", marker_color=colors))
        fig.add_vline(x=0, line_color="#263238")
        fig.update_layout(title="Sales gap versus target", xaxis_title="Gap (₹ lakh)")

    elif primary in {"Annotated line chart", "Line chart with target band"}:
        df = time_series_revenue()
        fig = go.Figure(go.Scatter(x=df["month"], y=df["revenue"], mode="lines", line={"color": PRIMARY, "width": 3}))
        peak = df.loc[df["revenue"].idxmax()]
        fig.add_annotation(
            x=peak["month"],
            y=peak["revenue"],
            text=f"Peak: ₹{peak['revenue']:.1f}L",
            showarrow=True,
            arrowhead=2,
            ay=-35,
        )
        if primary == "Line chart with target band":
            fig.add_hrect(y0=145, y1=165, fillcolor=ACCENT, opacity=0.12, line_width=0, annotation_text="Target band")
        fig.update_layout(title="Revenue trend with decision context", yaxis_title="Revenue (₹ lakh)")

    elif primary in {"Box plot with visible observations", "Distribution with reference line"}:
        df = customer_satisfaction()
        fig = px.box(df, x="department", y="nps_score", color="department", points="outliers")
        if primary == "Distribution with reference line":
            fig.add_hline(y=7, line_dash="dash", line_color=ACCENT, annotation_text="Target = 7")
        fig.update_layout(title="Customer score distribution by department", showlegend=False)

    elif primary == "Scatter plot with trend line":
        df = scatter_sales_spend()
        fig = px.scatter(df, x="marketing_spend", y="revenue", color="channel", trendline="ols")
        fig.update_layout(title="Marketing spend and revenue association")

    elif primary == "Histogram":
        df = customer_satisfaction()
        fig = px.histogram(df, x="nps_score", nbins=18)
        fig.update_traces(marker_color=PRIMARY)
        fig.update_layout(title="Distribution of customer scores")

    elif primary in {"Choropleth map", "Proportional-symbol map"}:
        geo = pd.DataFrame(
            {
                "city": ["Delhi", "Mumbai", "Bengaluru", "Kolkata", "Chennai", "Goa"],
                "lat": [28.61, 19.08, 12.97, 22.57, 13.08, 15.49],
                "lon": [77.21, 72.88, 77.59, 88.36, 80.27, 73.83],
                "value": [82, 96, 110, 65, 78, 48],
            }
        )
        fig = px.scatter_geo(
            geo,
            lat="lat",
            lon="lon",
            size="value",
            color="value",
            hover_name="city",
            scope="asia",
            projection="natural earth",
        )
        fig.update_geos(lataxis_range=[5, 38], lonaxis_range=[65, 100], fitbounds="locations")
        fig.update_layout(title="Illustrative regional demand")

    elif primary in {"Sankey diagram", "Network graph", "Adjacency matrix"}:
        fig = go.Figure(
            go.Sankey(
                node={"label": ["Website", "Store", "Cart", "Purchase", "Exit"]},
                link={
                    "source": [0, 0, 1, 1, 2, 2],
                    "target": [2, 4, 2, 4, 3, 4],
                    "value": [60, 40, 35, 15, 55, 40],
                },
            )
        )
        fig.update_layout(title="Customer journey flow")

    else:  # hierarchy
        hierarchy = pd.DataFrame(
            {
                "division": ["Consumer", "Consumer", "Enterprise", "Enterprise"],
                "category": ["Digital", "Retail", "Services", "Software"],
                "value": [42, 28, 18, 31],
            }
        )
        if primary == "Sunburst chart":
            fig = px.sunburst(hierarchy, path=["division", "category"], values="value")
        else:
            fig = px.treemap(hierarchy, path=["division", "category"], values="value")
        fig.update_layout(title="Revenue hierarchy by division and category")

    fig.update_layout(height=420, margin={"t": 60, "r": 25, "b": 45, "l": 55})
    return fig


def render_chart_engine() -> None:
    hero(
        "📊 Chart Selection Engine",
        "Describe the data, analytical question, and audience to receive a defensible chart recommendation.",
    )

    first, second, third, fourth = st.columns(4)
    data_type = first.selectbox(
        "Data structure",
        ["Categorical", "Numerical", "Time series", "Geospatial", "Relational", "Hierarchical"],
        key="ce_dtype",
    )
    question = second.selectbox(
        "Analytical question",
        ["Compare", "Rank", "Show trend", "Show distribution", "Show relationship", "Show composition", "Show deviation"],
        key="ce_question",
    )
    audience = third.selectbox(
        "Audience",
        ["Executive", "Analyst", "Operations manager", "Healthcare manager", "Customer / public"],
        key="ce_audience",
    )
    category_count = fourth.number_input(
        "Number of categories",
        min_value=2,
        max_value=50,
        value=5,
        help="Used when composition or categorical comparisons are involved.",
    )

    recommendation = get_recommendation(data_type, question, audience, int(category_count))

    st.markdown("### Recommended visual")
    primary_col, alternative_col = st.columns([1.1, 1])
    with primary_col:
        st.success(f"**Primary:** {recommendation.primary}", icon="✅")
        callout_insight(recommendation.rationale, "Why it fits")
    with alternative_col:
        st.markdown("#### Good alternatives")
        for alternative in recommendation.alternatives:
            st.markdown(f"- {alternative}")
        callout_mistake(recommendation.avoid, "Avoid")

    st.markdown("### Matching live example")
    figure = _example_figure(recommendation, data_type, question)
    st.plotly_chart(figure, use_container_width=True, config={"displaylogo": False, "responsive": True})
    st.caption("The example uses deterministic synthetic data. The recommendation—not visual novelty—should drive chart choice.")


def _safe_filename(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip().lower()).strip("_")
    return cleaned or "data_story"


def render_storytelling_builder() -> None:
    hero(
        "📝 Storytelling Framework Builder",
        "Develop a complete Context → Evidence → Insight → Recommendation → Action narrative.",
    )

    input_col, preview_col = st.columns([1.25, 1], gap="large")
    with input_col:
        domain = st.selectbox(
            "Business domain",
            ["Sales", "Marketing", "Operations", "Finance", "Healthcare", "HR", "Strategy"],
            key="sb_domain",
        )
        period = st.text_input("Time period", "Q3 2026", key="sb_period")
        context = st.text_area(
            "1. Context — what is the situation?",
            key="sb_context",
            height=90,
            placeholder="Revenue has declined for three quarters in the North and West regions.",
        )
        question = st.text_input(
            "2. Business question",
            key="sb_question",
            placeholder="Which region is underperforming, why, and what should change?",
        )
        evidence_1 = st.text_input("3. Evidence — key finding 1", key="sb_evidence_1")
        evidence_2 = st.text_input("Evidence — key finding 2", key="sb_evidence_2")
        evidence_3 = st.text_input("Evidence — key finding 3 (optional)", key="sb_evidence_3")
        pattern = st.text_area("4. Pattern — what connects the findings?", key="sb_pattern", height=75)
        insight = st.text_area("5. Insight — what does the pattern mean?", key="sb_insight", height=75)
        implication = st.text_area("6. Implication — what happens without action?", key="sb_implication", height=75)
        recommendation = st.text_area("7. Recommendation — what should be done?", key="sb_recommendation", height=90)
        action = st.text_input("8. Action — who does what, by when?", key="sb_action")

    evidence = [item for item in [evidence_1, evidence_2, evidence_3] if item.strip()]
    sections = [
        ("Context", context, "📌"),
        ("Business question", question, "❓"),
        ("Evidence", "\n".join(f"• {item}" for item in evidence), "📊"),
        ("Pattern", pattern, "🔍"),
        ("Insight", insight, "💡"),
        ("Implication", implication, "⚡"),
        ("Recommendation", recommendation, "🎯"),
        ("Action", action, "✅"),
    ]

    with preview_col:
        st.markdown("### Story preview")
        completed_sections = 0
        for label, content, icon in sections:
            st.markdown(f"**{icon} {label}**")
            if content.strip():
                completed_sections += 1
                st.markdown(f"> {content}")
            else:
                st.caption("Not completed yet")

        st.progress(completed_sections / len(sections), text=f"{completed_sections} of {len(sections)} story layers complete")

        required = [context, question, insight, recommendation, action]
        if all(item.strip() for item in required):
            story_text = f"""DATA STORY — {domain} | {period}
{'=' * 64}

CONTEXT
{context}

BUSINESS QUESTION
{question}

DATA EVIDENCE
{chr(10).join(f'• {item}' for item in evidence) if evidence else '[No evidence entered]'}

PATTERN
{pattern or '[Not entered]'}

INSIGHT
{insight}

IMPLICATION
{implication or '[Not entered]'}

RECOMMENDATION
{recommendation}

ACTION
{action}

---
Generated by Storytelling using Data Visualization
PGDM-BDA | Goa Institute of Management | Dr. Alok Tiwari
"""
            st.download_button(
                "Download story as text",
                story_text.encode("utf-8"),
                file_name=f"{_safe_filename(domain)}_data_story.txt",
                mime="text/plain",
                use_container_width=True,
            )
            callout_action(
                "Read the story aloud. Each layer should logically earn the next, and the action should name an owner and deadline.",
                "Quality check",
            )
        else:
            st.info("Complete Context, Business question, Insight, Recommendation, and Action to enable export.")


CASES = {
    "Sales performance": {
        "loader": regional_sales,
        "context": "A regional company is preparing its quarterly review and must decide where to reallocate sales support.",
        "questions": [
            "Which region has the largest actual-versus-target shortfall?",
            "Which product category contributes most to regional variation?",
            "What targeted resource action is supported by the evidence?",
        ],
    },
    "Marketing campaign ROI": {
        "loader": marketing_campaign,
        "context": "The CMO must rebalance next year's channel budget using return, conversion, and scale evidence.",
        "questions": [
            "Which channel has the highest ROI?",
            "Which high-spend channel underperforms?",
            "Where should the next incremental ₹10 lakh be allocated?",
        ],
    },
    "Operations delays": {
        "loader": operations_delays,
        "context": "The operations head needs to know whether delays are improving and which operational factor deserves investigation.",
        "questions": [
            "Is average delay improving over time?",
            "Is shipment volume associated with delay?",
            "What realistic six-month target should management adopt?",
        ],
    },
    "Finance cost control": {
        "loader": financial_expenses,
        "context": "The CFO needs a defensible view of cost structure and the categories driving change over eight quarters.",
        "questions": [
            "Which category accounts for the largest total cost?",
            "Which category is growing fastest?",
            "What cost action would have the largest impact without relying on an arbitrary cut?",
        ],
    },
    "Hospital capacity": {
        "loader": bed_occupancy,
        "context": "A hospital administrator must assess ward-level capacity pressure and whether overflow planning is justified.",
        "questions": [
            "Which ward has the highest average occupancy?",
            "How frequently does each ward exceed 85% occupancy?",
            "What operational response is supported by the pattern?",
        ],
    },
    "Channel strategy": {
        "loader": scatter_sales_spend,
        "context": "A retail brand is evaluating whether revenue response differs across online, offline, and blended channels.",
        "questions": [
            "Which channel shows the strongest spend–revenue association?",
            "Where do high-spend, low-return observations appear?",
            "What experiment should precede a major budget shift?",
        ],
    },
}


def _case_headline(case_name: str, df: pd.DataFrame) -> str:
    if case_name == "Sales performance":
        summary = df.groupby("region")[["sales", "target"]].sum()
        summary["gap"] = summary["sales"] - summary["target"]
        region = summary["gap"].idxmin()
        gap = abs(summary.loc[region, "gap"])
        return f"{region} has the largest target shortfall at ₹{gap:.0f} lakh"
    if case_name == "Marketing campaign ROI":
        best = df.loc[df["roi"].idxmax()]
        worst = df.loc[df["roi"].idxmin()]
        return f"{best['channel']} leads ROI; {worst['channel']} requires a budget challenge"
    if case_name == "Operations delays":
        start = df["avg_delay_hrs"].head(8).mean()
        end = df["avg_delay_hrs"].tail(8).mean()
        change = (end / start - 1) * 100
        direction = "improved" if change < 0 else "worsened"
        return f"Average delays {direction} by {abs(change):.1f}% from the opening to closing period"
    if case_name == "Finance cost control":
        totals = df.groupby("category")["amount_lakhs"].sum().sort_values(ascending=False)
        return f"{totals.index[0]} is the largest cost pool at ₹{totals.iloc[0]:.0f} lakh"
    if case_name == "Hospital capacity":
        average = df.groupby("ward")["occupancy_pct"].mean().sort_values(ascending=False)
        return f"{average.index[0]} has the highest average occupancy at {average.iloc[0]:.1f}%"

    correlations = df.groupby("channel").apply(
        lambda group: group["marketing_spend"].corr(group["revenue"]),
        include_groups=False,
    )
    channel = correlations.abs().idxmax()
    return f"{channel} shows the strongest spend–revenue association in the synthetic sample"


def _case_figure(case_name: str, df: pd.DataFrame) -> go.Figure:
    if case_name == "Sales performance":
        summary = df.groupby("region", as_index=False)[["sales", "target"]].sum()
        summary["gap"] = summary["sales"] - summary["target"]
        summary = summary.sort_values("gap")
        colors = [DANGER if value < 0 else SUCCESS for value in summary["gap"]]
        figure = go.Figure(go.Bar(x=summary["gap"], y=summary["region"], orientation="h", marker_color=colors))
        figure.add_vline(x=0, line_color="#263238")
        figure.update_layout(xaxis_title="Actual minus target (₹ lakh)")
    elif case_name == "Marketing campaign ROI":
        figure = px.scatter(df, x="spend_lakhs", y="roi", size="revenue_lakhs", color="channel", text="channel")
        figure.update_traces(textposition="top center")
    elif case_name == "Operations delays":
        figure = px.line(df, x="week", y="avg_delay_hrs", markers=True)
        figure.update_traces(line_color=PRIMARY)
        figure.add_hline(y=3, line_dash="dash", line_color=ACCENT, annotation_text="Illustrative 3-hour target")
    elif case_name == "Finance cost control":
        figure = px.bar(df, x="quarter", y="amount_lakhs", color="category", barnorm="percent")
        figure.update_layout(yaxis_title="Share of quarterly cost (%)")
    elif case_name == "Hospital capacity":
        average = df.groupby("ward", as_index=False)["occupancy_pct"].mean().sort_values("occupancy_pct")
        colors = [DANGER if value > 85 else WARNING if value > 75 else PRIMARY for value in average["occupancy_pct"]]
        figure = go.Figure(go.Bar(x=average["occupancy_pct"], y=average["ward"], orientation="h", marker_color=colors))
        figure.add_vline(x=85, line_dash="dash", line_color=DANGER, annotation_text="85% alert")
        figure.update_layout(xaxis_title="Average occupancy (%)")
    else:
        figure = px.scatter(df, x="marketing_spend", y="revenue", color="channel", trendline="ols")

    figure.update_layout(title=_case_headline(case_name, df), height=410, margin={"t": 70, "r": 25, "b": 45, "l": 55})
    return figure


def render_case_library() -> None:
    hero(
        "📚 Business Case Library",
        "Six guided cases with deterministic data, data-derived headlines, and management-focused questions.",
    )
    case_name = st.selectbox("Select case", list(CASES), key="case_name")
    case = CASES[case_name]
    df = case["loader"]().copy(deep=True)

    context_tab, evidence_tab, response_tab = st.tabs(["Case brief", "Evidence", "Your response"])
    with context_tab:
        st.markdown("### Business context")
        st.write(case["context"])
        st.info(f"**Data-derived headline:** {_case_headline(case_name, df)}")
        st.markdown("### Guided questions")
        for number, question in enumerate(case["questions"], 1):
            st.markdown(f"{number}. {question}")

    with evidence_tab:
        figure = _case_figure(case_name, df)
        st.plotly_chart(figure, use_container_width=True, config={"displaylogo": False})
        with st.expander("Inspect synthetic dataset"):
            st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "Download case dataset",
            df.to_csv(index=False).encode("utf-8"),
            file_name=f"{_safe_filename(case_name)}.csv",
            mime="text/csv",
        )

    with response_tab:
        st.markdown("### Construct the managerial story")
        for number, question in enumerate(case["questions"], 1):
            st.text_area(question, key=f"case_{_safe_filename(case_name)}_{number}", height=80)
        st.text_input("Action-oriented headline", key=f"case_headline_{_safe_filename(case_name)}")
        st.text_area(
            "Recommendation, owner, and deadline",
            key=f"case_recommendation_{_safe_filename(case_name)}",
            height=100,
        )
        with st.expander("Reveal a recommended approach"):
            callout_action(
                f"Start with the verified headline: **{_case_headline(case_name, df)}**. "
                "Use one overview chart, one diagnostic chart, and one action statement. "
                "Separate what the data proves from hypotheses that require further testing.",
                "Recommended structure",
            )


def _question_id(question: dict[str, object]) -> str:
    raw = f"{question['session']}|{question['type']}|{question['q']}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


def render_quiz_zone() -> None:
    hero(
        "❓ Quiz Zone",
        "Filter questions by session and type. Selections remain attached to the correct question when filters change.",
    )

    filter_col, type_col = st.columns(2)
    session_filter = filter_col.selectbox("Session", ["All"] + list(range(1, 17)), key="quiz_session_filter")
    type_filter = type_col.selectbox("Question type", ["All", "MCQ", "TrueFalse", "Scenario"], key="quiz_type_filter")

    questions = list(QUIZ_BANK)
    if session_filter != "All":
        questions = [question for question in questions if question["session"] == int(session_filter)]
    if type_filter != "All":
        questions = [question for question in questions if question["type"] == type_filter]

    answered = 0
    for question in questions:
        qid = _question_id(question)
        if st.session_state.get(f"quiz_choice_{qid}") is not None:
            answered += 1

    st.progress(answered / len(questions) if questions else 0, text=f"{answered} of {len(questions)} visible questions answered")

    if not questions:
        st.warning("No questions match the selected filters.")
        return

    for number, question in enumerate(questions, 1):
        qid = _question_id(question)
        title = f"Q{number} · Session {question['session']} · {question['clo']} · {question['type']}"
        with st.expander(title):
            st.markdown(f"**{question['q']}**")
            choice = st.radio(
                "Select your answer",
                question["options"],
                index=None,
                key=f"quiz_choice_{qid}",
            )
            if st.button("Check answer", key=f"quiz_check_{qid}"):
                st.session_state[f"quiz_revealed_{qid}"] = True

            if st.session_state.get(f"quiz_revealed_{qid}", False):
                if choice is None:
                    st.warning("Select an option before checking the answer.")
                elif choice == question["answer"]:
                    st.success(f"Correct. {question['explanation']}", icon="✅")
                else:
                    st.error(
                        f"Correct answer: **{question['answer']}**\n\n{question['explanation']}",
                        icon="❌",
                    )

    if st.button("Clear visible quiz responses"):
        for question in questions:
            qid = _question_id(question)
            st.session_state.pop(f"quiz_choice_{qid}", None)
            st.session_state.pop(f"quiz_revealed_{qid}", None)
        st.rerun()


def render_resources() -> None:
    hero(
        "🛠 Visualization Resources",
        "A focused set of tools for creating clear charts, dashboards, and visual stories.",
    )

    resources = [
        (
            "Tableau Public",
            "https://public.tableau.com",
            "Interactive dashboards, maps, and portfolio work. Public publishing is the default.",
            "Intermediate",
        ),
        (
            "Flourish",
            "https://flourish.studio",
            "Template-based animated charts, story maps, and scrollytelling without coding.",
            "Beginner",
        ),
        (
            "Datawrapper",
            "https://www.datawrapper.de",
            "Clean publication-ready charts and maps with strong defaults.",
            "Beginner",
        ),
        (
            "RAWGraphs",
            "https://rawgraphs.io",
            "Open-source exploration of alluvial, bump, streamgraph, and other less-common chart families.",
            "Beginner–intermediate",
        ),
        (
            "Google Sheets",
            "https://sheets.google.com",
            "Fast analysis and familiar charts for reports, group work, and classroom exercises.",
            "Beginner",
        ),
        (
            "Power BI Desktop",
            "https://powerbi.microsoft.com/desktop",
            "Business dashboards, data modelling, and reports connected to multiple sources.",
            "Intermediate",
        ),
    ]

    columns = st.columns(2)
    for index, (name, url, description, level) in enumerate(resources):
        with columns[index % 2]:
            with st.container(border=True):
                st.markdown(f"#### {name}")
                st.write(description)
                st.caption(f"Suggested level: {level}")
                st.link_button("Open official website", url, use_container_width=True)

    callout_insight(
        "Choose one primary tool and learn its workflow deeply. Use this app to strengthen chart reasoning; use the external tool to strengthen production skill.",
        "Tool strategy",
    )
    st.caption("External tools may change their plans or feature availability. Review the provider's current terms before use.")
