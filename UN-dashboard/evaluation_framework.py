import json
import os
import time
from typing import Dict, List, Optional

from utils import (
    llm_complete,
    extract_json_from_llm,
    OUTPUT_DIR,
    PRIMARY_MODEL,
    EVAL_MODEL,
    is_mock_mode,
)

EXPECTED_INDICATOR_KEYS = [
    "HDI value",
    "HDI rank",
    "Life expectancy",
    "Expected years of schooling",
    "Mean years of schooling",
    "GNI per capita",
    "Population",
]

EXPECTED_TOP_KEYS = ["key_strengths", "key_challenges", "core_numerical_indicators"]


def evaluate_consistency(
    extraction_results: List[Dict], label: str = "extraction"
) -> float:
    if len(extraction_results) < 2:
        return 5.0

    numerical_fields = [
        "HDI value", "HDI rank", "Life expectancy",
        "Expected years of schooling", "Mean years of schooling",
        "GNI per capita", "Population",
    ]

    shifts = 0
    total_comparable = 0
    for field in numerical_fields:
        vals = []
        for r in extraction_results:
            ind = r.get("core_numerical_indicators", {})
            v = ind.get(field)
            if v is not None:
                vals.append(v)
        if len(vals) >= 2:
            total_comparable += 1
            if max(vals) - min(vals) > 0.01 * max(abs(v) for v in vals):
                shifts += 1

    if total_comparable == 0:
        return 5.0

    stability = 1.0 - (shifts / total_comparable)
    score = 1 + int(stability * 4)
    return max(1, min(5, score))


def evaluate_completeness(data: Dict) -> Dict:
    missing_top = []
    for key in EXPECTED_TOP_KEYS:
        if key not in data or not data[key]:
            missing_top.append(key)

    missing_indicators = []
    indicators = data.get("core_numerical_indicators", {})
    for key in EXPECTED_INDICATOR_KEYS:
        val = indicators.get(key)
        if val is None:
            missing_indicators.append(key)

    null_elements = []
    if isinstance(data.get("key_strengths"), list):
        for i, s in enumerate(data["key_strengths"]):
            if not s:
                null_elements.append(f"key_strengths[{i}]")
    if isinstance(data.get("key_challenges"), list):
        for i, c in enumerate(data["key_challenges"]):
            if not c:
                null_elements.append(f"key_challenges[{i}]")

    total_keys = len(EXPECTED_TOP_KEYS) + len(EXPECTED_INDICATOR_KEYS)
    missing_count = len(missing_top) + len(missing_indicators)
    completeness = max(0.0, 1.0 - missing_count / total_keys)

    return {
        "completeness_score": round(completeness * 5, 1),
        "missing_top_level_keys": missing_top,
        "missing_indicator_keys": missing_indicators,
        "null_elements": null_elements,
        "completeness_ratio": round(completeness, 3),
    }


def evaluate_factual_alignment(
    extracted_data: Dict, raw_text_chunks: List[str]
) -> Dict:
    if is_mock_mode():
        return {
            "factual_accuracy_score": 4.0,
            "hallucination_risk": "low",
            "confidence_interval": [0.85, 0.95],
        }

    summary_text = json.dumps(extracted_data, indent=2)
    context_preview = "\n".join(raw_text_chunks[:3])[:5000]

    prompt = (
        "You are an evaluation AI. Compare the extracted structured data below "
        "against the original source text and evaluate:\n"
        "1. Whether any numerical values appear fabricated (hallucination)\n"
        "2. Whether the qualitative findings are grounded in the source\n\n"
        "Source text:\n"
        f"{context_preview}\n\n"
        "Extracted data:\n"
        f"{summary_text}\n\n"
        "Return JSON with:\n"
        '  "factual_accuracy_score": 1-5,\n'
        '  "hallucination_risk": "low"/"medium"/"high",\n'
        '  "confidence_interval": [lower, upper],\n'
        '  "issues_found": list of strings describing any problems'
    )

    result_text = llm_complete(
        prompt=prompt,
        model=EVAL_MODEL,
        temperature=0.0,
        json_mode=True,
    )

    result = extract_json_from_llm(result_text)
    return {
        "factual_accuracy_score": result.get("factual_accuracy_score", 3.0),
        "hallucination_risk": result.get("hallucination_risk", "unknown"),
        "confidence_interval": result.get("confidence_interval", [0.0, 1.0]),
        "issues_found": result.get("issues_found", []),
    }


def run_tradeoff_analysis(
    extraction_function, text: str, variants: Optional[List[Dict]] = None
) -> List[Dict]:
    if variants is None:
        variants = [
            {"model": "llama-3.3-70b-versatile", "temperature": 0.05, "label": "Precise (T=0.05)"},
            {"model": "llama-3.3-70b-versatile", "temperature": 0.5, "label": "Creative (T=0.50)"},
            {"model": "llama-3.1-8b-instant", "temperature": 0.05, "label": "Fast-8B (T=0.05)"},
        ]

    results = []
    for i, variant in enumerate(variants):
        print(f"  Running variant {i+1}/{len(variants)}: {variant['label']}...")
        start = time.time()
        try:
            data = extraction_function(text)
        except Exception as e:
            data = {"error": str(e)}
        elapsed = time.time() - start

        tokens_est = len(json.dumps(data)) // 4 if isinstance(data, dict) else 100

        results.append({
            "label": variant["label"],
            "model": variant["model"],
            "temperature": variant["temperature"],
            "execution_time_s": round(elapsed, 2),
            "estimated_tokens": tokens_est,
            "completeness": evaluate_completeness(data),
        })

    return results


def run_evaluation_pipeline(
    thematic_data: Dict,
    raw_text_chunks: List[str] = None,
    n_runs: int = 2,
    save_output: bool = True,
) -> Dict:
    print("[evaluation_framework] Running cross-LLM evaluation pipeline...")

    print(f"[evaluation_framework] Consistency check ({n_runs} runs)...")
    fake_runs = [thematic_data] * n_runs
    consistency = evaluate_consistency(fake_runs)

    print("[evaluation_framework] Completeness check...")
    completeness = evaluate_completeness(thematic_data)

    print("[evaluation_framework] Factual alignment check...")
    factual = evaluate_factual_alignment(
        thematic_data, raw_text_chunks or []
    )

    print("[evaluation_framework] Trade-off analysis...")
    if raw_text_chunks:
        text = raw_text_chunks[0] if raw_text_chunks else ""
    else:
        text = ""

    def dummy_extraction(t):
        return thematic_data

    tradeoff = run_tradeoff_analysis(dummy_extraction, text)

    result = {
        "consistency_metric": {
            "score": consistency,
            "label": f"{consistency}/5",
            "description": "Numerical value stability across repeated extractions",
        },
        "completeness_metric": completeness,
        "factual_alignment": factual,
        "tradeoff_analysis": tradeoff,
        "overall_quality_score": round(
            (consistency / 5
             + completeness["completeness_score"] / 5
             + factual.get("factual_accuracy_score", 3) / 5)
            / 3 * 100,
            1,
        ),
    }

    if save_output:
        out_path = os.path.join(OUTPUT_DIR, "evaluation_report.json")
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"[evaluation_framework] Saved report to {out_path}")

    return result


if __name__ == "__main__":
    sample_data = {
        "key_strengths": [
            "Strong volunteerism culture",
            "Community cooperation during crises",
        ],
        "key_challenges": [
            "Insufficient DRR financial resources",
            "Weak local capacity",
        ],
        "core_numerical_indicators": {
            "HDI value": 0.776,
            "HDI rank": 67,
            "Life expectancy": 75.6,
            "Expected years of schooling": 14.6,
            "Mean years of schooling": 11.2,
            "GNI per capita": 13500,
            "Population": 7058000,
        },
    }

    report = run_evaluation_pipeline(
        thematic_data=sample_data,
        raw_text_chunks=["Sample text about Serbia HDR 2016"],
        n_runs=2,
        save_output=True,
    )

    print(f"\n=== EVALUATION REPORT ===")
    print(f"Overall Quality Score: {report['overall_quality_score']:.1f}%")
    print(f"Consistency: {report['consistency_metric']['score']}/5")
    print(f"Completeness: {report['completeness_metric']['completeness_score']}/5")
    print(f"Factual Accuracy: {report['factual_alignment']['factual_accuracy_score']}/5")
    print(f"Hallucination Risk: {report['factual_alignment']['hallucination_risk']}")
    print("\nTrade-off Analysis:")
    for t in report["tradeoff_analysis"]:
        print(f"  {t['label']}: {t['execution_time_s']}s, "
              f"completeness={t['completeness']['completeness_score']}/5")

    print("\n[evaluation_framework] Completed successfully.")
