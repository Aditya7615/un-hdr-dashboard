import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
FEATURES_PATH = os.path.join(PROJECT_ROOT, '03_eda_cleaned', 'ipl_features.csv')

ALL_FEATURES = [
    'runs', 'wickets', 'matches',
    'batting_average', 'strike_rate', 'fours', 'sixes',
    'fifties', 'hundreds', 'catches',
    'bowling_average', 'economy_rate', 'bowling_strike_rate',
    'career_matches', 'seasons_played',
    'career_fifties', 'career_hundreds', 'career_catches',
]

BAT_FEATURES = [
    'runs', 'matches',
    'batting_average', 'strike_rate', 'fours', 'sixes',
    'fifties', 'hundreds', 'catches',
    'career_matches', 'seasons_played',
    'career_fifties', 'career_hundreds', 'career_catches',
]

BOWL_FEATURES = [
    'wickets', 'matches',
    'bowling_average', 'economy_rate', 'bowling_strike_rate',
    'catches', 'career_matches', 'seasons_played',
    'career_catches',
]

AR_FEATURES = ALL_FEATURES


def load_feature_data(path=None):
    if path is None:
        path = FEATURES_PATH
    return pd.read_csv(path)


def get_feature_columns(df):
    exclude = [
        'player_id', 'season', 'highest_score', 'best_bowling',
        'performance_category', '_outlier',
        'total_runs', 'total_wickets', 'batting_impact', 'bowling_impact',
        'consistency_score', 'overall_performance_score',
        'highest_score_num', 'highest_score_notout',
        'best_bowling_wickets', 'best_bowling_runs',
        'innings',
        'career_runs', 'career_wickets',
        'career_innings',
    ]
    return [c for c in df.columns if c not in exclude and df[c].dtype in (np.int64, np.float64)]


def classify_player(row):
    career_runs = row.get('career_runs', row.get('total_runs', 0))
    career_wickets = row.get('career_wickets', row.get('total_wickets', 0))
    if pd.isna(career_runs): career_runs = 0
    if pd.isna(career_wickets): career_wickets = 0
    if career_runs == 0 and career_wickets == 0:
        season_runs = row.get('runs', 0)
        season_wkts = row.get('wickets', 0)
        if pd.isna(season_runs): season_runs = 0
        if pd.isna(season_wkts): season_wkts = 0
        career_runs = season_runs
        career_wickets = season_wkts
    runs_weight = career_runs / (career_runs + career_wickets * 20 + 1)
    wkts_weight = career_wickets * 20 / (career_runs + career_wickets * 20 + 1)
    if runs_weight >= 0.7:
        return 'batsman'
    elif wkts_weight >= 0.7:
        return 'bowler'
    else:
        return 'all_rounder'


FEATURE_SETS = {
    'batsman': BAT_FEATURES,
    'bowler': BOWL_FEATURES,
    'all_rounder': AR_FEATURES,
}


def prepare_data(df, feat_cols=None, test_size=0.2, random_state=42):
    if feat_cols is None:
        feat_cols = get_feature_columns(df)
    X = df[feat_cols].fillna(0)
    y = df['overall_performance_score'].values
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state,
    )
    return X_train, X_test, y_train, y_test, feat_cols, X.columns.tolist()


def prepare_role_data(df, role, test_size=0.2, random_state=42):
    df_role = df.copy()
    df_role['player_role'] = df_role.apply(classify_player, axis=1)
    df_role = df_role[df_role['player_role'] == role]
    feat_cols = FEATURE_SETS[role]
    if len(df_role) == 0:
        return None, None, None, None, feat_cols
    X = df_role[feat_cols].fillna(0)
    y = df_role['overall_performance_score'].values
    if len(X) < 10:
        return None, None, None, None, feat_cols
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state,
    )
    return X_train, X_test, y_train, y_test, feat_cols


def get_features_for_role(role):
    return FEATURE_SETS.get(role, ALL_FEATURES)
