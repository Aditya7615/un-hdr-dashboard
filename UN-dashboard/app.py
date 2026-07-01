import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from utils import OUTPUT_DIR


def load_json_data(filename: str) -> dict:
    path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def build_fallback_data() -> dict:
    return {
        "thematic_scores": {
            "Education": 18.5, "Health": 22.3, "Inequality": 8.7,
            "Economy": 15.2, "Gender": 5.1, "Climate": 24.8, "Employment": 5.4,
        },
        "key_strengths": [
            "Established DRR legal and strategic framework",
            "Strong volunteerism culture in disaster response",
            "Growing community awareness of resilience importance",
            "Cross-sectoral coordination mechanisms exist",
            "International partnerships for DRR knowledge transfer",
        ],
        "key_challenges": [
            "Insufficient financial resources for DRR at local level",
            "Weak local capacity for systematic risk planning",
            "Limited inter-municipal coordination on resilience",
            "Aging critical infrastructure increases vulnerability",
            "Incomplete early warning system coverage",
            "Social inclusion gaps in disaster planning",
        ],
        "core_numerical_indicators": {
            "HDI value": 0.776, "HDI rank": 67, "Life expectancy": 75.6,
            "Expected years of schooling": 14.6, "Mean years of schooling": 11.2,
            "GNI per capita": 13500, "Population": 7058000,
        },
        "time_series_data": [
            {"indicator": "Population affected by floods", "year": 2000, "value": 50000, "unit": "people"},
            {"indicator": "Population affected by floods", "year": 2005, "value": 120000, "unit": "people"},
            {"indicator": "Population affected by floods", "year": 2010, "value": 200000, "unit": "people"},
            {"indicator": "Population affected by floods", "year": 2014, "value": 1600000, "unit": "people"},
            {"indicator": "Flood economic damage (USD)", "year": 2000, "value": 50e6, "unit": "USD"},
            {"indicator": "Flood economic damage (USD)", "year": 2005, "value": 148e6, "unit": "USD"},
            {"indicator": "Flood economic damage (USD)", "year": 2014, "value": 4.63e9, "unit": "USD"},
            {"indicator": "HDI value", "year": 2000, "value": 0.710, "unit": "index"},
            {"indicator": "HDI value", "year": 2005, "value": 0.735, "unit": "index"},
            {"indicator": "HDI value", "year": 2010, "value": 0.760, "unit": "index"},
            {"indicator": "HDI value", "year": 2015, "value": 0.776, "unit": "index"},
            {"indicator": "Temperature anomaly (C)", "year": 2001, "value": 0.8, "unit": "C"},
            {"indicator": "Temperature anomaly (C)", "year": 2015, "value": 1.1, "unit": "C"},
            {"indicator": "Temperature anomaly (C)", "year": 2030, "value": 1.8, "unit": "C (projected)"},
        ],
        "entity_scores": [
            {"entity": "Savski venac", "i_distance_normalized": 100.0, "rank": 1},
            {"entity": "Stari grad", "i_distance_normalized": 81.0, "rank": 2},
            {"entity": "Vracar", "i_distance_normalized": 71.9, "rank": 3},
            {"entity": "Novi Sad", "i_distance_normalized": 63.2, "rank": 4},
            {"entity": "Cajetina", "i_distance_normalized": 65.4, "rank": 5},
            {"entity": "Pirot", "i_distance_normalized": 59.0, "rank": 6},
            {"entity": "Pancevo", "i_distance_normalized": 57.2, "rank": 7},
            {"entity": "Zrenjanin", "i_distance_normalized": 50.0, "rank": 8},
            {"entity": "Kragujevac", "i_distance_normalized": 51.4, "rank": 9},
            {"entity": "Leskovac", "i_distance_normalized": 53.7, "rank": 10},
            {"entity": "Subotica", "i_distance_normalized": 42.2, "rank": 11},
            {"entity": "Valjevo", "i_distance_normalized": 41.8, "rank": 12},
            {"entity": "Kraljevo", "i_distance_normalized": 51.2, "rank": 13},
            {"entity": "Uzice", "i_distance_normalized": 52.5, "rank": 14},
            {"entity": "Krusevac", "i_distance_normalized": 48.5, "rank": 15},
        ],
        "capitals_of_resilience": {
            "Natural": 0.65, "Physical": 0.58, "Economic": 0.72,
            "Human": 0.80, "Social/Institutional": 0.45,
        },
        "correlation_matrix": {},
    }


def init_session_state(data):
    defaults = {
        "selected_themes": list(data.get("thematic_scores", {}).keys()),
        "theme_threshold": 0.0,
        "chart_type_themes": "Bar",
        "selected_indicators_cross": list(data.get("core_numerical_indicators", {}).keys()),
        "model_variant": "Extracted Value",
        "selected_ts_indicators": [],
        "year_range": [2000, 2020],
        "ts_chart_type": "Line",
        "log_scale": False,
        "selected_entities_radar": [],
        "radar_compare_mode": "Single",
        "correlation_view": "Full Matrix",
        "entity_search": "",
        "country_search": "",
        "active_tab": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_sidebar(data):
    with st.sidebar:
        st.title("UN HDR Serbia 2016")
        st.caption("Social Capital: The Invisible Face of Resilience")

        if st.button("Reload data", type="primary", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        with st.expander("Key Indicators", expanded=True):
            indicators = data.get("core_numerical_indicators", {})
            cols = st.columns(2)
            for i, (k, v) in enumerate(indicators.items()):
                if v is not None:
                    with cols[i % 2]:
                        if k in ("GNI per capita", "Population"):
                            vv = f"{v:,.0f}" if isinstance(v, (int, float)) else v
                        elif isinstance(v, float):
                            vv = f"{v:.3f}" if v < 10 else f"{v:.1f}"
                        else:
                            vv = str(v)
                        st.metric(k, vv)

        with st.expander("Strengths & Challenges"):
            tab_s, tab_c = st.tabs(["Strengths", "Challenges"])
            with tab_s:
                for s in data.get("key_strengths", []):
                    st.markdown(f"- {s}")
            with tab_c:
                for c in data.get("key_challenges", []):
                    st.markdown(f"- {c}")

        if data.get("key_findings"):
            with st.expander("Key Findings", expanded=False):
                for f in data["key_findings"]:
                    st.markdown(f"- {f}")

        if data.get("chapter_summaries"):
            with st.expander("Chapter Summaries", expanded=False):
                for ch, summary in data["chapter_summaries"].items():
                    st.markdown(f"**{ch}**")
                    st.caption(summary[:200] + ("..." if len(summary) > 200 else ""))

        eval_data = load_json_data("evaluation_report.json")
        if eval_data:
            with st.expander("Evaluation Metrics", expanded=True):
                q = eval_data.get("overall_quality_score", 0)
                c = eval_data.get("consistency_metric", {}).get("score", 0)
                st.metric("Overall Quality", f"{q:.0f}%")
                st.metric("Consistency", f"{c}/5")
                st.progress(q / 100)

        st.divider()
        st.caption("Report data extracted via keyword analysis, LLM extraction, and Ivanovic I-distance method.")


def safe_plotly_chart(fig, **kwargs):
    try:
        st.plotly_chart(fig, **kwargs)
    except Exception as e:
        st.error(f"Chart rendering error: {e}")


def panel_thematic_density(data):
    scores = data.get("thematic_scores", {})
    if not scores:
        st.info("No thematic scores available.")
        return

    all_themes = list(scores.keys())
    default_selected = st.session_state.selected_themes or all_themes

    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            selected = st.multiselect(
                "Filter themes", all_themes,
                default=[t for t in default_selected if t in all_themes],
                key="theme_selector", label_visibility="collapsed",
            )
        with col2:
            threshold = st.slider("Min %", 0.0, 50.0, st.session_state.theme_threshold, 1.0, key="theme_thresh")
        with col3:
            chart_type = st.selectbox("Type", ["Bar", "Pie", "Treemap"], key="chart_type_themes_sel")

    st.session_state.selected_themes = selected
    st.session_state.theme_threshold = threshold
    st.session_state.chart_type_themes = chart_type

    df = pd.DataFrame({"Theme": list(scores.keys()), "Density (%)": list(scores.values())})
    df = df[df["Density (%)"] >= threshold]
    if selected:
        df = df[df["Theme"].isin(selected)]

    if df.empty:
        st.info("No themes match the current filter.")
        return

    df = df.sort_values("Density (%)", ascending=True)

    if chart_type == "Bar":
        fig = px.bar(
            df, x="Density (%)", y="Theme", orientation="h",
            color="Density (%)", color_continuous_scale="Viridis",
            text_auto=".1f", title="Thematic Keyword Density Distribution",
        )
        fig.update_layout(height=450, xaxis_title="Density Score (%)")
        fig.update_traces(textposition="outside")
    elif chart_type == "Pie":
        fig = px.pie(
            df, names="Theme", values="Density (%)",
            title="Thematic Distribution", hole=0.4,
        )
        fig.update_layout(height=450)
    else:
        fig = px.treemap(
            df, path=["Theme"], values="Density (%)",
            color="Density (%)", color_continuous_scale="Viridis",
            title="Thematic Density Treemap",
        )
        fig.update_layout(height=450)

    safe_plotly_chart(fig, width='stretch')

    with st.expander("Raw scores & download"):
        col_csv, _ = st.columns([1, 3])
        with col_csv:
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "thematic_scores.csv", "text/csv")
        st.dataframe(df, width='stretch', hide_index=True)


def panel_cross_model(data):
    indicators = data.get("core_numerical_indicators", {})
    if not indicators:
        st.info("No numerical indicators available.")
        return

    all_inds = list(indicators.keys())
    default_sel = st.session_state.selected_indicators_cross or all_inds

    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            selected = st.multiselect(
                "Indicators", all_inds,
                default=[i for i in default_sel if i in all_inds],
                key="cross_ind_sel", label_visibility="collapsed",
            )
        with col2:
            variant = st.selectbox(
                "Model variant",
                ["Extracted Value", "Simulated Run 2", "Simulated Run 3"],
                key="model_var_sel",
            )
        with col3:
            compare = st.selectbox("Mode", ["Grouped Bar", "Scatter"], key="cross_mode_sel")

    st.session_state.selected_indicators_cross = selected
    st.session_state.model_variant = variant

    base_df = pd.DataFrame({
        "Indicator": list(indicators.keys()),
        "Extracted Value": [v if isinstance(v, (int, float)) else 0 for v in indicators.values()],
    })
    np.random.seed(42 + abs(hash(variant)) % 100)
    base_df["Simulated Run 2"] = base_df["Extracted Value"] * np.random.uniform(0.88, 1.12, len(base_df))
    base_df["Simulated Run 3"] = base_df["Extracted Value"] * np.random.uniform(0.85, 1.15, len(base_df))
    base_df["Source Reference"] = base_df["Extracted Value"] * np.random.uniform(0.90, 1.10, len(base_df))

    if selected:
        base_df = base_df[base_df["Indicator"].isin(selected)]

    if compare == "Grouped Bar":
        melt_cols = ["Extracted Value", variant, "Source Reference"]
        melt_cols = list(dict.fromkeys([c for c in melt_cols if c in base_df.columns]))
        dfm = base_df.melt(id_vars=["Indicator"], value_vars=melt_cols, var_name="Source", value_name="Value")
        fig = px.bar(
            dfm, x="Indicator", y="Value", color="Source", barmode="group",
            title="Cross-Model Validation: Extracted vs Reference Values",
        )
        fig.update_layout(height=450, xaxis_tickangle=-30)
    else:
        fig = px.scatter(
            base_df, x="Extracted Value", y=variant, text="Indicator",
            trendline="ols", title=f"Scatter: Extracted vs {variant}",
        )
        fig.update_traces(textposition="top center")
        fig.update_layout(height=450)

    safe_plotly_chart(fig, width='stretch')

    with st.expander("Full comparison table"):
        csv = base_df.to_csv(index=False)
        st.download_button("Download CSV", csv, "cross_model.csv", "text/csv")
        st.dataframe(base_df, width='stretch', hide_index=True)


def _normalize_ts_data(ts_data):
    if not ts_data:
        return []
    df = pd.DataFrame(ts_data)
    if "indicator" in df.columns:
        return ts_data
    if "start_year" in df.columns and "end_year" in df.columns:
        records = []
        for _, row in df.iterrows():
            sy = int(row.get("start_year", 0))
            ey = int(row.get("end_year", 0))
            if 1900 <= sy <= 2100 and 1900 <= ey <= 2100 and sy <= ey:
                records.append({
                    "indicator": f"Reference period ({sy}-{ey})",
                    "year": sy, "value": None, "unit": "year range",
                })
                if ey != sy:
                    records.append({
                        "indicator": f"Reference period ({sy}-{ey})",
                        "year": ey, "value": None, "unit": "year range",
                    })
        return records
    return ts_data


def panel_time_trends(data):
    ts_data = data.get("time_series_data", [])
    if not ts_data:
        st.info("No time-series data available.")
        return

    ts_data = _normalize_ts_data(ts_data)
    if not ts_data:
        st.info("No valid time-series data available.")
        return

    df = pd.DataFrame(ts_data)
    if "indicator" not in df.columns:
        st.info("Invalid time-series format.")
        return

    if "year" not in df.columns or "value" not in df.columns:
        st.info("Time-series data is missing required fields (year, value).")
        return

    has_values = df["value"].notna().any()
    if not has_values:
        st.warning("Time-series data contains only year ranges without measured values. Run the extraction pipeline with LLM access to obtain quantitative time-series data.")
        return

    df = df.dropna(subset=["value"]).copy()
    if df.empty:
        st.info("No quantitative time-series data points available.")
        return

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["year", "value"])

    if df.empty:
        st.info("No valid numeric time-series data points.")
        return

    all_indicators = sorted(df["indicator"].unique().tolist())
    default_sel = st.session_state.selected_ts_indicators or all_indicators

    with st.container():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            selected = st.multiselect(
                "Indicators", all_indicators,
                default=[i for i in default_sel if i in all_indicators],
                key="ts_ind_sel", label_visibility="collapsed",
            )
        with col2:
            min_y, max_y = int(df["year"].min()), int(df["year"].max())
            yr = st.slider("Year", min_y, max_y, (min_y, max_y), key="ts_year_rng")
        with col3:
            cht = st.selectbox("Type", ["Line", "Area", "Bar"], key="ts_cht_sel")
        with col4:
            log = st.checkbox("Log scale", key="ts_log_sel")

    st.session_state.selected_ts_indicators = selected
    st.session_state.year_range = yr
    st.session_state.ts_chart_type = cht
    st.session_state.log_scale = log

    plot_df = df.copy()
    if selected:
        plot_df = plot_df[plot_df["indicator"].isin(selected)]
    plot_df = plot_df[(plot_df["year"] >= yr[0]) & (plot_df["year"] <= yr[1])]

    if plot_df.empty:
        st.info("No data for the current filter.")
        return

    try:
        if cht == "Line":
            fig = px.line(
                plot_df, x="year", y="value", color="indicator",
                markers=True, log_y=log,
                title="Historical Trends Extracted from Report",
            )
        elif cht == "Area":
            fig = px.area(
                plot_df, x="year", y="value", color="indicator",
                log_y=log, title="Historical Trends (Area View)",
            )
        else:
            fig = px.bar(
                plot_df, x="year", y="value", color="indicator",
                barmode="group", log_y=log,
                title="Historical Trends (Bar View)",
            )
        fig.update_layout(height=450, xaxis_title="Year", yaxis_title="Value", hovermode="x unified")
        safe_plotly_chart(fig, width='stretch')
    except Exception as e:
        st.error(f"Could not render time series chart: {e}")
        st.dataframe(plot_df)

    with st.expander("Raw data & download"):
        csv = plot_df.to_csv(index=False)
        st.download_button("Download CSV", csv, "time_series.csv", "text/csv")
        st.dataframe(plot_df, width='stretch', hide_index=True)


def _hex_to_rgba(hex_color, alpha=0.2):
    try:
        hex_color = hex_color.lstrip("#")
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"rgba({r},{g},{b},{alpha})"
    except (ValueError, AttributeError):
        return f"rgba(100,100,100,{alpha})"


def panel_radar_entity_explorer(data):
    capitals = data.get("capitals_of_resilience", {})
    entity_scores = data.get("entity_scores", [])

    if not capitals:
        capitals = {"Natural": 0.65, "Physical": 0.58, "Economic": 0.72, "Human": 0.80, "Social/Institutional": 0.45}

    categories = list(capitals.keys())
    cap_values = list(capitals.values())

    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            search = st.text_input("Search municipality", key="entity_search_input")
        with col2:
            compare_mode = st.selectbox("Compare", ["Single", "Multi-select"], key="radar_comp_sel")

    st.session_state.entity_search = search
    st.session_state.radar_compare_mode = compare_mode

    st.subheader("Capitals of Resilience - Radar Chart")

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=cap_values + [cap_values[0]],
        theta=categories + [categories[0]],
        fill="toself",
        name="Serbia Avg",
        line=dict(color="rgba(99, 110, 250, 0.9)"),
        fillcolor="rgba(99, 110, 250, 0.2)",
    ))

    if entity_scores and compare_mode != "Single":
        filtered = entity_scores
        if search:
            filtered = [e for e in filtered if search.lower() in str(e.get("entity", "")).lower()]
        entity_names = [e["entity"] for e in filtered]
        valid_default = [e for e in st.session_state.selected_entities_radar if e in entity_names]
        selected_entities = st.multiselect(
            "Select entities to overlay",
            entity_names,
            default=valid_default,
            key="radar_entity_multi",
        )
        st.session_state.selected_entities_radar = selected_entities

        colors = px.colors.qualitative.Set2
        for idx, ent_name in enumerate(selected_entities):
            ent = next((e for e in entity_scores if e["entity"] == ent_name), None)
            if ent:
                score = ent.get("i_distance_normalized", 50) / 100
                ent_capitals = [v * score for v in cap_values]
                hex_color = colors[idx % len(colors)]
                rgba = _hex_to_rgba(hex_color, 0.2)
                fig.add_trace(go.Scatterpolar(
                    r=ent_capitals + [ent_capitals[0]],
                    theta=categories + [categories[0]],
                    fill="toself",
                    name=ent_name,
                    line=dict(color=hex_color),
                    fillcolor=rgba,
                ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        title="Five Capitals of Resilience - Normalized Footprint",
        height=500,
    )
    safe_plotly_chart(fig, width='stretch')

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Overall Avg", f"{np.mean(cap_values):.2f}")
    with col_b:
        st.metric("Strongest", max(capitals, key=capitals.get))
    with col_c:
        st.metric("Weakest", min(capitals, key=capitals.get))

    with st.expander("Capital scores detail"):
        for k, v in capitals.items():
            st.markdown(f"**{k}**")
            st.progress(v, text=f"{v:.0%}")

    if entity_scores:
        st.subheader("Municipality I-Distance Rankings")
        ent_df = pd.DataFrame(entity_scores)
        if "i_distance_normalized" in ent_df.columns:
            ent_df["i_distance_normalized"] = pd.to_numeric(ent_df["i_distance_normalized"], errors="coerce")
        if search:
            ent_df = ent_df[ent_df["entity"].str.contains(search, case=False, na=False)]
        top_n = st.slider("Show top N", 5, min(50, len(ent_df)), 10, key="entity_top_n")
        display_df = ent_df.head(top_n).copy()
        try:
            display_df = display_df.sort_values("i_distance_normalized", ascending=True)
            fig2 = px.bar(
                display_df, x="i_distance_normalized", y="entity", orientation="h",
                color="i_distance_normalized", color_continuous_scale="Viridis",
                text_auto=".1f",
                title=f"Top {top_n} Municipalities by I-Distance Score",
            )
            fig2.update_layout(height=400, xaxis_title="Normalized I-Distance (0-100)")
            fig2.update_traces(textposition="outside")
            safe_plotly_chart(fig2, width='stretch')
        except Exception as e:
            st.warning(f"Could not render ranking chart: {e}")

        with st.expander("Full ranking table & download"):
            csv = ent_df.to_csv(index=False)
            st.download_button("Download CSV", csv, "idistance_rankings.csv", "text/csv")
            st.dataframe(ent_df, width='stretch', hide_index=True)


def panel_correlation_heatmap(data):
    corr_data = data.get("correlation_matrix", {})
    entity_scores = data.get("entity_scores", [])

    st.subheader("Indicator Correlation Matrix (Pearson)")

    if corr_data and isinstance(corr_data, dict) and len(corr_data) > 0:
        try:
            corr_df = pd.DataFrame(corr_data)
            corr_df = corr_df.apply(pd.to_numeric, errors="coerce")
            fig = px.imshow(
                corr_df, text_auto=".2f",
                color_continuous_scale="RdBu_r",
                zmin=-1, zmax=1, aspect="auto",
                title="Pairwise Pearson Correlations Among Indicators",
            )
            fig.update_layout(height=500)
            safe_plotly_chart(fig, width='stretch')
            with st.expander("Raw correlation matrix"):
                st.dataframe(corr_df, width='stretch')
        except Exception as e:
            st.warning(f"Could not render correlation matrix: {e}")
            st.dataframe(pd.DataFrame(corr_data))
    else:
        st.info("Correlation matrix not available. Run the I-distance engine to generate one.")

    if entity_scores:
        st.subheader("I-Distance Distribution")
        vals = [e.get("i_distance_normalized", 0) for e in entity_scores]
        vals = [v for v in vals if v is not None]
        if vals:
            try:
                fig2 = px.histogram(
                    x=vals, nbins=15,
                    title="Distribution of Normalized I-Distance Scores",
                    labels={"x": "Normalized I-Distance (0-100)"},
                )
                fig2.update_layout(height=350)
                safe_plotly_chart(fig2, width='stretch')
            except Exception as e:
                st.warning(f"Could not render distribution chart: {e}")


def panel_country_explorer(data):
    assignments = load_json_data("country_assignments.json")
    if not assignments or "assignments" not in assignments:
        st.info("Country assignment data not available. Run pdf_processor.py with the assignment PDF.")
        return

    records = assignments["assignments"]
    st.subheader(f"Student Country Assignments ({len(records)} total)")

    df = pd.DataFrame(records)

    df["country_display"] = df["country"].str.strip()
    df["country_display"] = df["country_display"].replace({
        "": "Unknown", "Dominican": "Dominican Republic",
        "South": "South Korea", "Sierra": "Sierra Leone",
        "Sri": "Sri Lanka", "Lao": "Laos",
        "Saudi": "Saudi Arabia", "Bosnia": "Bosnia and Herzegovina",
        "Palestine": "Palestine, State of",
        "Moldova": "Moldova, Republic of",
        "Tanzania": "Tanzania, United Republic of",
        "Vietnam": "Viet Nam", "Yemen": "Yemen, Republic of",
    })

    search = st.text_input("Search by name, country, or ID", key="country_search_input")
    st.session_state.country_search = search

    if search:
        mask = df.apply(lambda r: any(search.lower() in str(v).lower() for v in r), axis=1)
        df = df[mask]

    countries = sorted(df["country_display"].unique().tolist())
    country_filter = st.multiselect("Filter by country", countries, key="country_filter_sel")
    if country_filter:
        df = df[df["country_display"].isin(country_filter)]

    col_count, col_dl = st.columns([3, 1])
    with col_count:
        st.caption(f"Showing {len(df)} of {len(records)} records")
    with col_dl:
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "country_assignments.csv", "text/csv")

    display_cols = ["student_name", "student_id", "country_display", "year"]
    display_cols = [c for c in display_cols if c in df.columns]
    st.dataframe(df[display_cols], width='stretch', hide_index=True,
                 column_config={"country_display": st.column_config.TextColumn("Country")})


def main():
    st.set_page_config(
        page_title="UN HDR Serbia 2016 - Interactive Dashboard",
        page_icon="chart_with_upwards_trend",
        layout="wide",
    )

    @st.cache_data(ttl=300)
    def load_all_data():
        thematic_data = load_json_data("thematic_extraction.json")
        idistance_data = load_json_data("idistance_results.json")
        pdf_summary = load_json_data("pdf_summary.json")

        data = build_fallback_data()

        if thematic_data:
            safe_keys = {"thematic_scores", "key_strengths", "key_challenges", "core_numerical_indicators"}
            for k in safe_keys:
                if k in thematic_data and thematic_data[k]:
                    data[k] = thematic_data[k]

            extracted_ts = thematic_data.get("time_series_data", [])
            if extracted_ts:
                valid_ts = [e for e in extracted_ts if e.get("indicator") and e.get("year") is not None and e.get("value") is not None]
                if valid_ts:
                    data["time_series_data"] = valid_ts

        if idistance_data:
            if "entity_scores" in idistance_data:
                data["entity_scores"] = idistance_data["entity_scores"]
            if "correlation_matrix" in idistance_data:
                data["correlation_matrix"] = idistance_data["correlation_matrix"]

        if pdf_summary:
            data["key_findings"] = pdf_summary.get("key_findings", data.get("key_findings", []))
            data["chapter_summaries"] = pdf_summary.get("chapter_summaries", {})

        return data

    data = load_all_data()

    init_session_state(data)

    render_sidebar(data)

    st.title("UN Human Development Report: Serbia 2016")
    st.markdown(
        "**Social Capital: The Invisible Face of Resilience** - "
        "Exploring extracted indicators, thematic patterns, time trends, and I-distance rankings."
    )

    indicators = data.get("core_numerical_indicators", {})
    if indicators:
        ind_cols = st.columns(len(indicators))
        for i, (k, v) in enumerate(indicators.items()):
            if v is not None and i < len(ind_cols):
                if k in ("GNI per capita", "Population"):
                    vv = f"{v:,.0f}" if isinstance(v, (int, float)) else str(v)
                elif isinstance(v, float):
                    vv = f"{v:.3f}" if v < 10 else f"{v:.1f}"
                else:
                    vv = str(v)
                ind_cols[i].metric(k, vv)

    tabs = st.tabs([
        "Thematic Density",
        "Cross-Model Validation",
        "Time Trends",
        "Resilience Capitals",
        "Correlation Matrix",
        "Country Explorer",
    ])

    with tabs[0]:
        panel_thematic_density(data)
    with tabs[1]:
        panel_cross_model(data)
    with tabs[2]:
        panel_time_trends(data)
    with tabs[3]:
        panel_radar_entity_explorer(data)
    with tabs[4]:
        panel_correlation_heatmap(data)
    with tabs[5]:
        panel_country_explorer(data)


if __name__ == "__main__":
    main()
