import os, sys, json, joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from data_utils import load_feature_data, get_feature_columns
from data_utils import FEATURE_SETS, ALL_FEATURES

MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models'))

st.set_page_config(
    page_title="CricPredict — Player Performance Analyzer",
    page_icon=":cricket_game:",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def load_artifacts():
    results_path = os.path.join(MODELS_DIR, 'all_models_results.pkl')
    meta_path = os.path.join(MODELS_DIR, 'metadata.json')
    comp_path = os.path.join(MODELS_DIR, 'model_comparison.csv')
    if not os.path.exists(results_path):
        return None, None, None
    results = joblib.load(results_path)
    with open(meta_path) as f:
        metadata = json.load(f)
    comp_df = pd.read_csv(comp_path) if os.path.exists(comp_path) else None
    return results, metadata, comp_df


@st.cache_resource
def load_role_models():
    role_dir = os.path.join(MODELS_DIR, 'role_models')
    role_models = {}
    for role in ['batsman', 'bowler', 'all_rounder']:
        models = {}

        lgb_path = os.path.join(role_dir, role, 'lgb_model.pkl')
        meta_path = os.path.join(role_dir, role, 'metadata.json')
        if os.path.exists(lgb_path) and os.path.exists(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
            models['LightGBM'] = {
                'model': joblib.load(lgb_path),
                'features': meta['features'],
                'r2_score': meta['r2_score'],
                'mae': meta['mae'],
                'rmse': meta['rmse'],
            }

        ens_path = os.path.join(role_dir, role, 'ensemble_model.pkl')
        ens_meta_path = os.path.join(role_dir, role, 'ensemble_metadata.json')
        if os.path.exists(ens_path) and os.path.exists(ens_meta_path):
            with open(ens_meta_path) as f:
                meta = json.load(f)
            models['Ensemble'] = {
                'model': joblib.load(ens_path),
                'features': meta['features'],
                'r2_score': meta['r2_score'],
                'mae': meta['mae'],
                'rmse': meta['rmse'],
            }

        xgb_path = os.path.join(role_dir, role, 'xgb_model.pkl')
        if os.path.exists(xgb_path):
            with open(meta_path) as f:
                meta = json.load(f)
            models['XGBoost'] = {
                'model': joblib.load(xgb_path),
                'features': meta['features'],
                'r2_score': meta.get('r2_score', 0),
                'mae': meta.get('mae', 0),
                'rmse': meta.get('rmse', 0),
            }

        if models:
            role_models[role] = models
    return role_models


@st.cache_resource
def load_data():
    try:
        return load_feature_data()
    except FileNotFoundError:
        return None


results, metadata, comp_df = load_artifacts()
df_full = load_data()
role_models = load_role_models()

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main > div { padding: 1.5rem 2rem; }
    .hero {
        background: linear-gradient(135deg, #0D2137 0%, #1A3A4A 50%, #0D2137 100%);
        border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2rem;
        border: 1px solid rgba(0, 212, 170, 0.15); position: relative; overflow: hidden;
    }
    .hero::before {
        content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(0, 212, 170, 0.03) 0%, transparent 50%);
        pointer-events: none;
    }
    .hero h1 { color: #FFFFFF; font-size: 2.2rem; font-weight: 800; margin: 0 0 0.3rem 0; letter-spacing: -0.5px; }
    .hero .subtitle { color: rgba(255,255,255,0.6); font-size: 1rem; font-weight: 300; margin: 0; }
    .hero .badge {
        display: inline-block; background: rgba(0, 212, 170, 0.15); color: #00D4AA;
        padding: 0.25rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500;
        border: 1px solid rgba(0, 212, 170, 0.3); margin-top: 0.8rem;
    }
    .card {
        background: #1A1D27; border-radius: 12px; padding: 1.5rem;
        border: 1px solid rgba(255,255,255,0.06); margin-bottom: 1rem;
    }
    .card h3 { color: #FFFFFF; font-size: 1rem; font-weight: 600; margin: 0 0 1rem 0; letter-spacing: 0.3px; text-transform: uppercase; opacity: 0.7; }
    .role-badge {
        display: inline-block; padding: 0.2rem 0.8rem; border-radius: 12px;
        font-size: 0.75rem; font-weight: 600; margin-left: 0.5rem;
    }
    .badge-batsman { background: rgba(74, 158, 255, 0.2); color: #4A9EFF; border: 1px solid rgba(74, 158, 255, 0.3); }
    .badge-bowler { background: rgba(255, 107, 107, 0.2); color: #FF6B6B; border: 1px solid rgba(255, 107, 107, 0.3); }
    .badge-allrounder { background: rgba(0, 212, 170, 0.2); color: #00D4AA; border: 1px solid rgba(0, 212, 170, 0.3); }
    .stButton button {
        background: linear-gradient(135deg, #00D4AA 0%, #00B894 100%) !important;
        color: #FFFFFF !important; font-weight: 600 !important; border: none !important;
        border-radius: 8px !important; padding: 0.6rem 2rem !important; font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(0, 212, 170, 0.3) !important;
    }
    div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; }
    div[data-testid="stMetricLabel"] { font-size: 0.8rem !important; opacity: 0.6 !important; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem; background: #1A1D27; border-radius: 10px; padding: 0.3rem;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .stTabs [data-baseweb="tab"] { border-radius: 8px !important; padding: 0.5rem 1.2rem !important; font-weight: 500 !important; }
    .stTabs [aria-selected="true"] { background: #00D4AA !important; color: #000 !important; }
    .info-box {
        background: rgba(0, 212, 170, 0.06); border-left: 3px solid #00D4AA;
        border-radius: 6px; padding: 0.8rem 1rem; margin: 0.5rem 0 1rem 0;
        font-size: 0.85rem; color: rgba(255,255,255,0.7);
    }
    .feature-chip {
        display: inline-block; background: rgba(255,255,255,0.06); border-radius: 4px;
        padding: 0.15rem 0.5rem; margin: 0.15rem; font-size: 0.75rem;
        font-family: 'SF Mono', monospace; color: rgba(255,255,255,0.7);
    }
</style>
"""


def score_to_category(score):
    score = np.clip(score, 0, 10)
    if score >= 8.0: return "Elite", "#00D4AA"
    if score >= 6.5: return "Very Good", "#4ADE80"
    if score >= 5.0: return "Good", "#FBBF24"
    if score >= 3.5: return "Average", "#FB923C"
    if score >= 2.0: return "Below Average", "#F97316"
    return "Poor", "#FF6B6B"


def create_gauge(score, color="#00D4AA"):
    score = np.clip(score, 0, 10)
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        number={
            'suffix': " / 10", 'font': {'size': 42, 'color': '#FFFFFF', 'family': 'Inter'},
        },
        delta={'reference': 5, 'increasing': {'color': '#00D4AA'}, 'decreasing': {'color': '#FF6B6B'}},
        gauge={
            'axis': {
                'range': [0, 10], 'tickwidth': 1, 'tickcolor': "rgba(255,255,255,0.3)",
                'tickfont': {'size': 11, 'color': 'rgba(255,255,255,0.5)'},
                'tickvals': [0, 2, 3.5, 5, 6.5, 8, 10],
                'ticktext': ['0', 'Poor', '', 'Avg', '', 'Good', '10'],
            },
            'bar': {'color': color, 'thickness': 0.45},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 2], 'color': 'rgba(255,107,107,0.12)'},
                {'range': [2, 3.5], 'color': 'rgba(249,115,22,0.12)'},
                {'range': [3.5, 5], 'color': 'rgba(251,146,60,0.12)'},
                {'range': [5, 6.5], 'color': 'rgba(251,191,36,0.12)'},
                {'range': [6.5, 8], 'color': 'rgba(74,222,128,0.12)'},
                {'range': [8, 10], 'color': 'rgba(0,212,170,0.12)'},
            ],
            'threshold': {
                'line': {'color': "white", 'width': 3},
                'thickness': 0.6, 'value': score,
            }
        },
    ))
    fig.update_layout(
        height=300, margin=dict(l=30, r=30, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)', font={'color': 'white'},
    )
    return fig


def render_role_badge(role):
    cls = {'batsman': 'badge-batsman', 'bowler': 'badge-bowler', 'all_rounder': 'badge-allrounder'}
    labels = {'batsman': 'BAT', 'bowler': 'BOWL', 'all_rounder': 'AR'}
    return f'<span class="role-badge {cls.get(role, "")}">{labels.get(role, role.upper())}</span>'


# ── Load ──
results, metadata, comp_df = load_artifacts()
df_full = load_data()
role_models = load_role_models()

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ── Hero ──
st.markdown("""
<div class="hero">
    <h1>:cricket_game: CricPredict</h1>
    <p class="subtitle">Role-Aware Performance Analyzer — predicts player performance using only relevant stats</p>
    <span class="badge">:sparkles: Ensemble &bull; XGBoost &bull; LightGBM — Role-Aware</span>
</div>
""", unsafe_allow_html=True)

if results is None:
    st.warning("No trained models found. Run: `python 04_modeling_and_deployment/scripts/train_all_models.py`")
    st.stop()

# ── Sidebar ──
with st.sidebar:
    st.markdown("### :crossed_swords: Player Role")
    st.markdown(
        "<p style='font-size:0.8rem; opacity:0.6; margin-bottom:0.5rem;'>"
        "Role determines which stats are used for prediction.</p>",
        unsafe_allow_html=True,
    )

    role_descriptions = {
        'batsman': 'Pure batter — no bowling stats used (no penalty for zero wickets)',
        'all_rounder': 'Bats & bowls — full stats considered for genuine all-rounders',
        'bowler': 'Primary bowler — bowling + fielding stats, batting excluded',
    }
    selected_role = st.radio(
        "Player Type",
        ['batsman', 'all_rounder', 'bowler'],
        index=0,
        format_func=lambda x: {
            'batsman': 'Batsman',
            'all_rounder': 'All-Rounder',
            'bowler': 'Bowler',
        }[x],
        help=role_descriptions.get('batsman', ''),
    )
    st.caption(role_descriptions[selected_role])

    st.markdown("---")
    st.markdown("### :gear: Model Selection")

    role_model_available = selected_role in role_models

    model_options = []
    if role_model_available:
        for sub_model in role_models[selected_role]:
            model_options.append(f"{sub_model} ({selected_role})")
    for gm in sorted(results.keys()):
        model_options.append(f"{gm} (general)")

    selected_model = st.selectbox("Choose model", model_options, index=0)
    is_role_model = role_model_available and f"({selected_role})" in selected_model

    if is_role_model:
        sub_model_name = selected_model.split(" (")[0]
        col1, col2, col3 = st.columns(3)
        rm = role_models[selected_role][sub_model_name]
        col1.metric("R²", f"{rm['r2_score']:.4f}")
        col2.metric("MAE", f"{rm['mae']:.3f}")
        col3.metric("RMSE", f"{rm['rmse']:.3f}")
    else:
        model_key = selected_model.split(" (")[0]
        if model_key in results:
            col1, col2, col3 = st.columns(3)
            md = results[model_key]
            col1.metric("R²", f"{md['metrics']['r2_score']:.4f}")
            col2.metric("MAE", f"{md['metrics']['mae']:.3f}")
            col3.metric("RMSE", f"{md['metrics']['rmse']:.3f}")

    st.markdown("---")
    st.markdown("### :bar_chart: Leaderboard")

    if comp_df is not None:
        sorted_comp = comp_df.sort_values('R²', ascending=False)
        for i, (_, row) in enumerate(sorted_comp.iterrows()):
            medal = {0: ":trophy:", 1: ":2nd_place_medal:", 2: ":3rd_place_medal:"}.get(i, ":small_blue_diamond:")
            highlight = "opacity:1.0" if row['Model'] == selected_model else "opacity:0.6"
            st.markdown(
                f"<div style='{highlight}'>"
                f"{medal} **{row['Model']}**  \n"
                f"R²: `{row['R²']:.4f}` &nbsp; MAE: `{row['MAE']:.4f}`"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")
    st.markdown("### :bulb: How It Works")
    st.markdown(
        "<p style='font-size:0.8rem; opacity:0.7;'>"
        "<b>Batsman</b> — 14 batting + career features<br>"
        "<b>Bowler</b> — 9 bowling + career features<br>"
        "<b>All-Rounder</b> — 18 features (bat + bowl + career)<br><br>"
        "No penalty for batsmen with zero bowling stats. "
        "Bowlers who bat get full credit via All-Rounder mode.</p>",
        unsafe_allow_html=True,
    )

# ── Determine features for the selected role ──
role_features = FEATURE_SETS.get(selected_role, ALL_FEATURES)
has_batting = any(f in role_features for f in ['batting_average', 'strike_rate'])
has_bowling = any(f in role_features for f in ['bowling_average', 'economy_rate'])
has_career_bat = any(f in role_features for f in ['career_fifties', 'career_hundreds'])

# ── Feature ranges for defaults ──
feature_ranges = {}
if df_full is not None:
    for f in ALL_FEATURES:
        if f in df_full.columns:
            feature_ranges[f] = {
                'min': float(df_full[f].min()),
                'max': float(df_full[f].max()),
                'mean': float(df_full[f].mean()),
                'median': float(df_full[f].median()),
            }

# ── Tabs ──
tab1, tab2, tab3 = st.tabs([":crossed_swords: Predict", ":chart_with_upwards_trend: Model Analysis", ":bar_chart: Explorer"])

# ═══════════════════════════════════════════════
# TAB 1 — PREDICT
# ═══════════════════════════════════════════════
with tab1:
    role_label = {'batsman': 'Batsman', 'all_rounder': 'All-Rounder', 'bowler': 'Bowler'}[selected_role]
    st.markdown(
        f"<div class='card'>"
        f"<h3>Player Statistics — {role_label} {render_role_badge(selected_role)}</h3>",
        unsafe_allow_html=True,
    )

    chips = ''.join(f'<span class="feature-chip">{f}</span>' for f in role_features)
    st.markdown(
        f"<div class='info-box'>"
        f"Using <strong>{len(role_features)} features</strong> for {role_label} role: "
        f"{chips}</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])

    input_data = {}

    with col1:
        st.markdown("**Batting**")
        if has_batting:
            input_data['runs'] = st.number_input(
                "Runs (season)", 0, 2000,
                value=int(feature_ranges.get('runs', {}).get('median', 350)),
                step=10, key="runs")
            input_data['matches'] = st.number_input(
                "Matches (season)", 0, 30,
                value=int(feature_ranges.get('matches', {}).get('median', 10)),
                step=1, key="matches")
            input_data['batting_average'] = st.number_input(
                "Batting Average", 0.0, 100.0,
                value=float(feature_ranges.get('batting_average', {}).get('median', 25)),
                step=0.5, format="%.1f", key="ba")
            input_data['strike_rate'] = st.number_input(
                "Strike Rate", 0.0, 300.0,
                value=float(feature_ranges.get('strike_rate', {}).get('median', 125)),
                step=0.5, format="%.1f", key="sr")
            input_data['fours'] = st.number_input(
                "Fours", 0, 100,
                value=int(feature_ranges.get('fours', {}).get('median', 12)),
                step=1, key="4s")
            input_data['sixes'] = st.number_input(
                "Sixes", 0, 100,
                value=int(feature_ranges.get('sixes', {}).get('median', 5)),
                step=1, key="6s")
        else:
            st.caption("Not used for this role")

    with col2:
        st.markdown("**Milestones & Fielding**")
        if has_batting:
            input_data['fifties'] = st.number_input(
                "Fifties (season)", 0, 50,
                value=int(feature_ranges.get('fifties', {}).get('median', 2)),
                step=1, key="50s")
            input_data['hundreds'] = st.number_input(
                "Hundreds (season)", 0, 20,
                value=int(feature_ranges.get('hundreds', {}).get('median', 0)),
                step=1, key="100s")
        input_data['catches'] = st.number_input(
            "Catches (season)", 0, 50,
            value=int(feature_ranges.get('catches', {}).get('median', 4)),
            step=1, key="ct")

        st.markdown("**Bowling**")
        if has_bowling:
            input_data['wickets'] = st.number_input(
                "Wickets (season)", 0, 100,
                value=int(feature_ranges.get('wickets', {}).get('median', 8)),
                step=1, key="wkts")
            input_data['bowling_average'] = st.number_input(
                "Bowling Average", 0.0, 100.0,
                value=float(feature_ranges.get('bowling_average', {}).get('median', 28)),
                step=0.5, format="%.1f", key="bowl_avg")
            input_data['economy_rate'] = st.number_input(
                "Economy Rate", 0.0, 20.0,
                value=float(feature_ranges.get('economy_rate', {}).get('median', 8.0)),
                step=0.1, format="%.1f", key="econ")
            input_data['bowling_strike_rate'] = st.number_input(
                "Bowling Strike Rate", 0.0, 50.0,
                value=float(feature_ranges.get('bowling_strike_rate', {}).get('median', 22)),
                step=0.5, format="%.1f", key="bowl_sr")
        else:
            st.caption("Not used — won't penalize batsmen")

    with col3:
        st.markdown("**Career**")
        if 'career_matches' in role_features:
            input_data['career_matches'] = st.number_input(
                "Career Matches", 0, 500,
                value=int(feature_ranges.get('career_matches', {}).get('median', 60)),
                step=5, key="cmat")
        if 'seasons_played' in role_features:
            input_data['seasons_played'] = st.number_input(
                "Seasons Played", 1, 20,
                value=int(feature_ranges.get('seasons_played', {}).get('median', 5)),
                step=1, key="sns")
        if has_career_bat:
            input_data['career_fifties'] = st.number_input(
                "Career Fifties", 0, 100,
                value=int(feature_ranges.get('career_fifties', {}).get('median', 8)),
                step=1, key="c50s")
            input_data['career_hundreds'] = st.number_input(
                "Career Hundreds", 0, 50,
                value=int(feature_ranges.get('career_hundreds', {}).get('median', 1)),
                step=1, key="c100s")
        if 'catches' not in input_data or 'career_catches' in role_features:
            input_data['career_catches'] = st.number_input(
                "Career Catches", 0, 200,
                value=int(feature_ranges.get('career_catches', {}).get('median', 15)),
                step=1, key="cct")

    st.markdown("</div>", unsafe_allow_html=True)

    # Predict button
    predict_col1, predict_col2, predict_col3 = st.columns([1, 2, 1])
    with predict_col2:
        predict_clicked = st.button(
            "PREDICT PERFORMANCE", type="primary", width='stretch'
        )

    if predict_clicked:
        if is_role_model:
            sub_model_name = selected_model.split(" (")[0]
            role_model_data = role_models[selected_role][sub_model_name]
            model = role_model_data['model']
            pred_features = role_model_data['features']
            model_name = selected_model
        else:
            model_key = selected_model.split(" (")[0]
            model_data = results[model_key]
            model = model_data['model']
            pred_features = role_features
            model_name = selected_model

        X_input = pd.DataFrame([input_data])[pred_features].fillna(0)

        X_input_val = X_input.values

        try:
            y_pred = model.predict(X_input_val) if hasattr(model, 'predict') else [0]
            pred_score = float(y_pred[0])
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            pred_score = 0.0

        category, cat_color = score_to_category(pred_score)

        # Results display
        res_col1, res_col2 = st.columns([1, 1.2])
        with res_col1:
            st.plotly_chart(create_gauge(pred_score, cat_color), width='stretch')

        with res_col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {cat_color}15, {cat_color}08);
                        border: 1px solid {cat_color}40; border-radius: 12px;
                        padding: 2rem; height: 100%; display: flex; flex-direction: column;
                        justify-content: center;">
                <p style="color: rgba(255,255,255,0.35); font-size: 0.8rem; margin: 0;
                          text-transform: uppercase; letter-spacing: 1.5px;">Predicted Performance</p>
                <p style="color: {cat_color}; font-size: 3.5rem; font-weight: 800;
                          margin: 0.2rem 0; line-height: 1.1;">{pred_score:.2f}<span style="font-size:1.2rem; font-weight:400; opacity:0.4;"> /10</span></p>
                <p style="color: #FFFFFF; font-size: 1.4rem; font-weight: 600;
                          margin: 0 0 0.3rem 0;">{category}</p>
                <div style="margin-top: 0.5rem;">
                    <span style="opacity:0.5; font-size:0.8rem;">Model:</span>
                    <span style="color:#00D4AA; font-size:0.85rem; font-weight:500;">{model_name}</span>
                    <span style="opacity:0.3; margin:0 0.5rem;">|</span>
                    <span style="opacity:0.5; font-size:0.8rem;">Role:</span>
                    <span style="color:#FFFFFF; font-size:0.85rem; font-weight:500;">{role_label}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Input summary
        st.markdown(
            "<div class='card' style='margin-top: 1rem;'>"
            "<h3>Input Summary</h3>",
            unsafe_allow_html=True,
        )
        display_df = pd.DataFrame([input_data]).T.rename(columns={0: "Value"})
        display_df.index.name = "Feature"
        st.dataframe(display_df, width='stretch')

        # Feature contribution note
        used = [f for f in pred_features if f in input_data]
        missing = [f for f in pred_features if f not in input_data]
        if missing:
            st.caption(f"Features set to 0 (not provided): {', '.join(missing)}")
        st.markdown("</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════
# TAB 2 — MODEL ANALYSIS
# ═══════════════════════════════════════════════
with tab2:
    st.markdown(
        f"<div class='card'><h3>Performance Metrics — {selected_model} {render_role_badge(selected_role) if is_role_model else ''}</h3>",
        unsafe_allow_html=True,
    )

    if is_role_model:
        sub_model_name = selected_model.split(" (")[0]
        rm = role_models[selected_role][sub_model_name]
        metrics_data = [
            ("R² Score", f"{rm['r2_score']:.4f}", "#00D4AA"),
            ("MAE", f"{rm['mae']:.4f}", "#4ADE80"),
            ("RMSE", f"{rm['rmse']:.4f}", "#FBBF24"),
            ("Features", str(len(rm['features'])), "#4A9EFF"),
        ]
    else:
        model_key = selected_model.split(" (")[0]
        md = results[model_key]
        metrics_data = [
            ("R² Score", f"{md['metrics']['r2_score']:.4f}", "#00D4AA"),
            ("MAE", f"{md['metrics']['mae']:.4f}", "#4ADE80"),
            ("RMSE", f"{md['metrics']['rmse']:.4f}", "#FBBF24"),
            ("Training Time", f"{md['time']:.1f}s", "#4A9EFF"),
        ]

    cols = st.columns(len(metrics_data))
    for ci, (label, value, color) in enumerate(metrics_data):
        with cols[ci]:
            st.markdown(
                f"<div style='background: rgba(0,0,0,0.2); border-radius: 10px; padding: 1rem; text-align: center;'>"
                f"<p style='color: rgba(255,255,255,0.4); font-size: 0.75rem; margin: 0; text-transform: uppercase;'>{label}</p>"
                f"<p style='color: {color}; font-size: 1.8rem; font-weight: 700; margin: 0.2rem 0;'>{value}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # Comparison charts
    col_left, col_right = st.columns([1, 1])
    with col_left:
        st.markdown("<div class='card'><h3>R² Score Comparison</h3>", unsafe_allow_html=True)
        if comp_df is not None:
            all_models_r2 = []
            for _, r in comp_df.iterrows():
                all_models_r2.append({'Model': f"{r['Model']} (general)", 'R²': r['R²'], 'source': 'General'})
            for role, sub_models in role_models.items():
                for sm_name, sm_data in sub_models.items():
                    all_models_r2.append({
                        'Model': f"{sm_name} ({role})",
                        'R²': sm_data['r2_score'],
                        'source': 'Role',
                    })

            r2_df = pd.DataFrame(all_models_r2)
            hl_model = selected_model

            colors = ['#00D4AA' if m == hl_model else
                      'rgba(0,212,170,0.35)' if '(batsman)' in m or '(bowler)' in m or '(all_rounder)' in m else 'rgba(255,255,255,0.2)'
                      for m in r2_df['Model']]

            fig = go.Figure(go.Bar(
                x=r2_df['Model'], y=r2_df['R²'],
                marker_color=colors,
                text=r2_df['R²'].round(3),
                textposition='outside', textfont={'size': 10},
            ))
            fig.update_layout(
                height=350, margin=dict(l=20, r=20, t=10, b=80),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis={'title': '', 'tickfont': {'color': 'rgba(255,255,255,0.6)', 'size': 10}},
                yaxis={'title': 'R²', 'tickfont': {'color': 'rgba(255,255,255,0.4)'},
                       'gridcolor': 'rgba(255,255,255,0.05)', 'range': [0, 1]},
                showlegend=False,
            )
            st.plotly_chart(fig, width='stretch')
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='card'><h3>Error Metrics</h3>", unsafe_allow_html=True)
        if comp_df is not None:
            fig = go.Figure()
            fig.add_trace(go.Bar(name='MAE', x=comp_df['Model'], y=comp_df['MAE'],
                                 marker_color='#FB923C', text=comp_df['MAE'].round(3),
                                 textposition='outside'))
            fig.add_trace(go.Bar(name='RMSE', x=comp_df['Model'], y=comp_df['RMSE'],
                                 marker_color='#FF6B6B', text=comp_df['RMSE'].round(3),
                                 textposition='outside'))
            fig.update_layout(
                barmode='group', height=350,
                margin=dict(l=20, r=20, t=10, b=40),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis={'title': '', 'tickfont': {'color': 'rgba(255,255,255,0.6)'}},
                yaxis={'title': 'Error', 'tickfont': {'color': 'rgba(255,255,255,0.4)'},
                       'gridcolor': 'rgba(255,255,255,0.05)'},
                legend={'font': {'color': 'rgba(255,255,255,0.6)'}},
            )
            st.plotly_chart(fig, width='stretch')
        st.markdown("</div>", unsafe_allow_html=True)

    # Expanders
    with st.expander("Best Parameters"):
        if is_role_model:
            sub_model_name = selected_model.split(" (")[0]
            st.json({"model": sub_model_name, "role": selected_role, "features": role_models[selected_role][sub_model_name]['features']})
        else:
            model_key = selected_model.split(" (")[0]
            st.json(results[model_key].get('params', {}))

    with st.expander("Feature Set Detail"):
        if is_role_model:
            sub_model_name = selected_model.split(" (")[0]
            feats = role_models[selected_role][sub_model_name]['features']
        else:
            feats = metadata['features'] if metadata else []
        st.markdown(f"**{len(feats)} Features Used:**")
        cols = st.columns(3)
        for i, f in enumerate(feats):
            cols[i % 3].markdown(f"- `{f}`")
        if is_role_model:
            st.info(f"Role-aware model: only {selected_role}-relevant features are used. "
                    f"This prevents irrelevant stats from affecting predictions.")

    with st.expander("Role-Aware Models Detail"):
        for role in ['batsman', 'bowler', 'all_rounder']:
            if role in role_models:
                st.markdown(f"**{role.title()}**")
                for sm_name, sm_data in role_models[role].items():
                    st.markdown(
                        f"  - **{sm_name}**: R²={sm_data['r2_score']:.4f}, MAE={sm_data['mae']:.4f}, "
                        f"{len(sm_data['features'])} features"
                    )

    with st.expander("Dataset Information"):
        if metadata:
            st.markdown(f"- **Train samples:** {metadata['train_samples']:,}")
            st.markdown(f"- **Test samples:** {metadata['test_samples']:,}")
            st.markdown(f"- **Total features:** {metadata['n_features']}")
            st.markdown(f"- **Players:** {df_full['player_id'].nunique() if df_full is not None else 'N/A':,}")


# ═══════════════════════════════════════════════
# TAB 3 — EXPLORER
# ═══════════════════════════════════════════════
with tab3:
    if df_full is not None:
        num_cols = df_full.select_dtypes(include=np.number).columns.tolist()
        cats = [c for c in df_full.columns if c not in num_cols and df_full[c].nunique() < 20]

        st.markdown("<div class='card'><h3>Feature Explorer</h3>", unsafe_allow_html=True)

        exp_col1, exp_col2, exp_col3 = st.columns([1, 1, 1])
        with exp_col1:
            col_x = st.selectbox("X-axis", num_cols,
                                 index=num_cols.index('runs') if 'runs' in num_cols else 0)
        with exp_col2:
            col_y = st.selectbox("Y-axis", num_cols,
                                 index=num_cols.index('overall_performance_score') if 'overall_performance_score' in num_cols else 1)
        with exp_col3:
            color_opts = cats + [c for c in num_cols if c not in (col_x, col_y)]
            col_color = st.selectbox("Color by", color_opts, index=0)

        sample_df = df_full.sample(min(1000, len(df_full)), random_state=42)

        fig = px.scatter(
            sample_df, x=col_x, y=col_y, color=col_color,
            title=f"{col_y} vs {col_x}",
            opacity=0.6, height=500,
            template='plotly_dark',
            color_continuous_scale='viridis' if col_color in num_cols else None,
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'rgba(255,255,255,0.7)'},
            xaxis={'gridcolor': 'rgba(255,255,255,0.05)'},
            yaxis={'gridcolor': 'rgba(255,255,255,0.05)'},
        )
        st.plotly_chart(fig, width='stretch')
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'><h3>Data Sample</h3>", unsafe_allow_html=True)
        st.dataframe(df_full.head(100), width='stretch')
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Feature data not found. Ensure 03_eda_cleaned/ipl_features.csv exists.")

# ── Footer ──
st.markdown(
    "<div style='text-align: center; padding: 2rem 0 0 0; opacity: 0.25; font-size: 0.75rem;'>"
    "CricPredict — Role-Aware Player Performance Analyzer &mdash; "
    f"Built with Streamlit &bull; {datetime.now().strftime('%Y')}</div>",
    unsafe_allow_html=True,
)
