# CricPredict — Player Performance Analyzer

**Group 1 — Team Project**  
Role-aware ML system that predicts cricket player performance scores (0–10) from batting and bowling statistics.

## The Problem

Two critical issues were identified and fixed in this project:

1. **Inverted Bowling Impact** — The `bowling_impact` formula had a division-by-zero bug (`wickets=0` divided by near-zero avg/econ produced scores of 10.0 for non-bowlers and 0.0 for bowlers, inverting the metric). Correlation flipped from **−0.67 → +0.91** after the fix.

2. **Role Confusion** — All players were evaluated on all 13 features regardless of role. Batsmen were penalized for zero bowling stats, and bowlers who batted had their batting contributions diluted. The fix uses **role-aware models** that select features based on player type.

## Solution: Role-Aware Prediction

| Role | Features | What's Used |
|------|----------|-------------|
| **Batsman** | 10 batting-only | No bowling stats → no penalty for zero wickets |
| **All-Rounder** | 13 full | Both batting and bowling stats for genuine dual-threat players |
| **Bowler** | 5 bowling + fielding | Bowling-focused, no irrelevant batting stats |

## Model Performance

### General Models

| Model | R² | MAE | RMSE |
|-------|-----|-----|------|
| XGBoost | **0.9805** | 0.0768 | 0.1092 |
| LightGBM | **0.9803** | 0.0771 | 0.1097 |
| Ensemble (XGB+LGB) | 0.9762 | 0.0797 | 0.1205 |

### Role-Aware Models

| Role | Model | R² | MAE | Features |
|------|-------|-----|-----|----------|
| Batsman | **Ensemble** | **0.9807** | 0.0678 | 14 |
| Batsman | XGBoost | 0.9786 | 0.0733 | 14 |
| Batsman | LightGBM | 0.9784 | 0.0727 | 14 |
| Bowler | **Ensemble** | **0.9527** | 0.0890 | 9 |
| Bowler | LightGBM | 0.9518 | 0.0932 | 9 |
| All-Rounder | LightGBM | 0.9069 | 0.1369 | 18 |

Key to high accuracy: the target formula uses `runs × batting_avg × SR` for batting impact,
`wickets / (bowling_avg × econ)` for bowling impact, and `seasons_played` / `career_matches` for
consistency — all of which are now included as model features. Artificial noise was also removed.

## Project Structure

```
project cricket/
├── README.md                         ← this file
├── .gitignore
│
├── 01_raw_data_and_scrapers/         ← Raw data + scrapers
│   ├── ipl_batting_fielding_stats.csv
│   ├── bcci_stats_rankings_all.csv
│   ├── generate_ipl_data.py
│   └── bcci_stats_scraper.py
│
├── 02_documentation_and_eda/         ← EDA notebooks & docs
│   ├── notebooks/01_eda.ipynb
│   ├── docs/ (Project_Plan, Test_Plan)
│   └── requirements.txt
│
├── 03_eda_cleaned/                   ← Processed data
│   ├── ipl_cleaned.csv
│   ├── ipl_features.csv             ← Features + target (fixed)
│   └── 01_eda_cleaned.ipynb
│
└── 04_modeling_and_deployment/       ← Training + Streamlit app
    ├── app/app.py                    ← Role-aware prediction UI
    ├── scripts/
    │   ├── data_utils.py             ← Feature sets, role classification
    │   ├── train_all_models.py       ← Full training pipeline
    │   └── models/
    │       ├── lightgbm_model.py     ← Role-aware backbone (recommended)
    │       ├── xgboost_model.py
    │       ├── random_forest.py
    │       ├── mlp_model.py
    │       ├── hybrid_model.py
    │       └── tabpfn_model.py
    ├── models/                       ← Trained artifacts (generated)
    │   ├── role_models/
    │   │   ├── batsman/lgb_model.pkl
    │   │   ├── bowler/lgb_model.pkl
    │   │   └── all_rounder/lgb_model.pkl
    │   ├── best_model.pkl
    │   └── model_comparison.csv
    ├── docs/ (Model_Card, Training_Report, Test_Plan)
    ├── notebooks/01_model_training.ipynb
    └── requirements.txt
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r "04_modeling_and_deployment/requirements.txt"
pip install -r "02_documentation_and_eda/requirements.txt"
```

### 2. Train all models

```bash
python "04_modeling_and_deployment/scripts/train_all_models.py"
```

This trains 5 general models + 3 role-aware LightGBM models and saves them to `04_modeling_and_deployment/models/`.

### 3. Launch the app

```bash
streamlit run "04_modeling_and_deployment/app/app.py"
```

Open **http://localhost:8501** in your browser.

## How to Use the App

1. **Select Role** (sidebar) — Batsman, All-Rounder, or Bowler
2. **Enter Stats** — Only relevant fields appear based on role
3. **Pick Model** — Defaults to LightGBM (role-specific, recommended)
4. **Predict** — Get a performance score with gauge visualization

## Feature Engineering

The target variable `overall_performance_score` [0–10] is a composite:

- **40% Batting Impact** — runs × average × strike rate (normalized)
- **30% Bowling Impact** — wickets / (average × economy) (normalized, **zero for non-bowlers**)
- **30% Consistency Score** — seasons played, total matches, run consistency

## Data Sources

- **IPL Stats:** Sports Mechanic API (2008–2026), ~733 unique players
- **BCCI Stats:** BCCI.tv (TEST, ODI, T20I formats)

## Key Bug Fixes

| Bug | Impact | Fix |
|-----|--------|-----|
| `bowling_impact` inverted (non-bowlers got 10.0, bowlers got 0.0) | Target variable was completely wrong | Added `wickets > 0` guard before computing bowling impact |
| All players used all 13 features | Batsmen penalized for zero bowling stats | Role-aware feature selection + separate models per role |
| TabPFN underperformed for cricket data | Low predictions, slow training | Replaced with LightGBM as role-aware backbone |
