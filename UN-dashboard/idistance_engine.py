import json
import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy import stats

from utils import OUTPUT_DIR

try:
    import pingouin as pg
    PINGOUIN_AVAILABLE = True
except ImportError:
    PINGOUIN_AVAILABLE = False


def normalize_minmax(values: List[float]) -> List[float]:
    arr = np.array(values, dtype=float)
    min_v, max_v = np.nanmin(arr), np.nanmax(arr)
    if max_v == min_v:
        return [0.5] * len(arr)
    return ((arr - min_v) / (max_v - min_v)).tolist()


def reorient(values: List[float]) -> List[float]:
    return [1.0 - v for v in values]


def compute_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    if PINGOUIN_AVAILABLE:
        return pg.rcorr(df, upper=False, decimals=4)
    return df.corr(method="pearson")


def compute_partial_correlation(
    x: np.ndarray, y: np.ndarray, covars: Optional[np.ndarray] = None
) -> float:
    if covars is None or covars.shape[1] == 0:
        corr, _ = stats.pearsonr(x, y)
        return corr
    n = len(x)
    X = np.column_stack([np.ones(n), covars, x])
    Y = np.column_stack([np.ones(n), covars, y])
    beta_x = np.linalg.lstsq(X, y, rcond=None)[0]
    beta_y = np.linalg.lstsq(Y, x, rcond=None)[0]
    res_x = y - X @ beta_x
    res_y = x - Y @ beta_y
    corr, _ = stats.pearsonr(res_x, res_y)
    return corr


def rank_indicators_by_variance(df: pd.DataFrame) -> List[str]:
    variances = df.var().sort_values(ascending=False)
    return variances.index.tolist()


def compute_idistance(
    data_matrix: np.ndarray,
    entity_names: List[str],
    indicator_names: List[str],
    base_index: int = 0,
) -> Tuple[np.ndarray, List[float]]:
    n_entities, k = data_matrix.shape
    y_base = data_matrix[base_index]

    if k == 1:
        distances = np.abs(data_matrix[:, 0] - y_base[0]) / max(np.std(data_matrix[:, 0]), 1e-10)
        return distances.reshape(-1, 1), distances.tolist()

    sigma = np.std(data_matrix, axis=0)
    sigma = np.where(sigma < 1e-10, 1e-10, sigma)

    distances = np.zeros((n_entities, k))
    for i in range(n_entities):
        d_raw = np.abs(data_matrix[i] - y_base)
        distances[i, 0] = d_raw[0] / sigma[0]

        for m in range(1, k):
            product = 1.0
            for j in range(m):
                idx_j = j
                idx_m = m
                if j > 0:
                    covar_cols = list(range(1, j))
                    covars = data_matrix[:, covar_cols] if covar_cols else None
                else:
                    covars = None

                partial_r = compute_partial_correlation(
                    data_matrix[:, idx_j],
                    data_matrix[:, idx_m],
                    covars,
                )
                product *= (1.0 - abs(partial_r))

            distances[i, m] = (d_raw[m] / sigma[m]) * product

    synthetic_scores = np.sum(distances, axis=1)
    return distances, synthetic_scores.tolist()


def build_idistance_pipeline(
    df: pd.DataFrame,
    entity_col: str = "entity",
    negative_indicators: Optional[List[str]] = None,
    base_entity: Optional[str] = None,
    save_output: bool = True,
) -> Dict:
    print("[idistance_engine] Starting I-distance calculation pipeline...")

    if negative_indicators is None:
        negative_indicators = []

    meta = df[[entity_col]].copy()
    indicators = [c for c in df.columns if c != entity_col]

    normalized_data = {}
    for col in indicators:
        vals = df[col].dropna().tolist()
        if col in negative_indicators:
            vals = reorient(vals)
        norm = normalize_minmax(vals)
        normalized_data[col] = norm

    norm_df = pd.DataFrame(normalized_data)

    print(f"[idistance_engine] Normalized {len(indicators)} indicators across {len(df)} entities")

    print("[idistance_engine] Computing correlation matrix...")
    corr_matrix = norm_df.corr(method="pearson")

    print("[idistance_engine] Ranking indicators by variance...")
    ranked = rank_indicators_by_variance(norm_df)
    ranked_df = norm_df[ranked]

    if base_entity is not None and base_entity in df[entity_col].values:
        base_idx = df[df[entity_col] == base_entity].index[0]
    else:
        base_idx = norm_df.apply(np.sum).idxmin()
        if isinstance(base_idx, str):
            base_idx = 0

    print(f"[idistance_engine] Computing I-distance (base entity index: {base_idx})...")
    step_distances, synthetic_scores = compute_idistance(
        ranked_df.values, df[entity_col].tolist(), ranked, base_idx
    )

    entity_scores = sorted(
        zip(df[entity_col].tolist(), synthetic_scores),
        key=lambda x: -x[1],
    )

    print("[idistance_engine] Normalizing final scores to 0-100 scale...")
    scores_arr = np.array(synthetic_scores)
    min_s, max_s = np.min(scores_arr), np.max(scores_arr)
    if max_s > min_s:
        normalized_scores = ((scores_arr - min_s) / (max_s - min_s) * 100).tolist()
    else:
        normalized_scores = [50.0] * len(scores_arr)

    score_df = pd.DataFrame({
        entity_col: df[entity_col],
        "i_distance_raw": synthetic_scores,
        "i_distance_normalized": normalized_scores,
    }).sort_values("i_distance_raw", ascending=False).reset_index(drop=True)
    score_df["rank"] = range(1, len(score_df) + 1)

    result = {
        "entity_count": len(df),
        "indicator_count": len(indicators),
        "indicator_ranking": ranked,
        "negative_indicators_reoriented": negative_indicators,
        "correlation_matrix": corr_matrix.round(4).to_dict(),
        "entity_scores": score_df.to_dict(orient="records"),
        "normalized_scores_0_100": {
            row[entity_col]: round(row["i_distance_normalized"], 2)
            for _, row in score_df.iterrows()
        },
    }

    if save_output:
        out_path = os.path.join(OUTPUT_DIR, "idistance_results.json")
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, default=str, ensure_ascii=False)
        print(f"[idistance_engine] Saved results to {out_path}")

    return result


def create_sample_dataset() -> pd.DataFrame:
    np.random.seed(42)
    municipalities = [
        "Savski venac", "Stari grad", "Vracar", "Novi Sad", "Cajetina",
        "Pirot", "Pancevo", "Zrenjanin", "Kragujevac", "Nis",
        "Subotica", "Cacak", "Valjevo", "Smederevo", "Leskovac",
        "Vranje", "Sombor", "Kraljevo", "Uzice", "Krusevac",
    ]
    data = {
        "entity": municipalities,
        "HDI_value": np.random.uniform(0.65, 0.85, 20).round(3).tolist(),
        "life_expectancy": np.random.uniform(72, 78, 20).round(1).tolist(),
        "expected_schooling": np.random.uniform(12, 15, 20).round(1).tolist(),
        "gni_per_capita": np.random.uniform(8000, 18000, 20).round(0).astype(int).tolist(),
        "population_density": np.random.uniform(20, 500, 20).round(1).tolist(),
        "unemployment_rate": np.random.uniform(8, 25, 20).round(1).tolist(),
        "flood_risk_score": np.random.uniform(10, 90, 20).round(1).tolist(),
    }
    return pd.DataFrame(data)


if __name__ == "__main__":
    print("[idistance_engine] Running with sample municipality data...")
    sample_df = create_sample_dataset()

    negative_indicators = ["unemployment_rate", "flood_risk_score"]

    result = build_idistance_pipeline(
        df=sample_df,
        entity_col="entity",
        negative_indicators=negative_indicators,
        save_output=True,
    )

    print(f"\n=== I-DISTANCE RESULTS ===")
    print(f"Entities: {result['entity_count']}")
    print(f"Indicators: {result['indicator_count']}")
    print(f"Indicator ranking (by variance): {result['indicator_ranking']}")
    print(f"\nTop 5 entities by I-distance:")
    for row in result["entity_scores"][:5]:
        print(f"  #{row['rank']} {row['entity']}: {row['i_distance_normalized']:.2f}")
    print(f"\nBottom 5 entities:")
    for row in result["entity_scores"][-5:]:
        print(f"  #{row['rank']} {row['entity']}: {row['i_distance_normalized']:.2f}")

    print("\n[idistance_engine] Completed successfully.")
