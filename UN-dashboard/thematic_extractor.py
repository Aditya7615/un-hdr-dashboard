import json
import os
import re
from typing import Dict, List

from utils import (
    llm_complete,
    extract_json_from_llm,
    OUTPUT_DIR,
    PRIMARY_MODEL,
)


CORE_THEMES = [
    "Education",
    "Health",
    "Inequality",
    "Economy",
    "Gender",
    "Climate",
    "Employment",
]

THEME_KEYWORDS = {
    "Education": [
        "school", "education", "literacy", "student", "teacher", "training",
        "learning", "enrollment", "dropout", "educational attainment",
        "preschool", "primary school", "secondary school", "university",
    ],
    "Health": [
        "health", "hospital", "doctor", "mortality", "life expectancy",
        "disease", "tuberculosis", "healthcare", "medical", "patient",
        "disability", "nutrition", "sanitation",
    ],
    "Inequality": [
        "inequality", "poverty", "gini", "disparity", "exclusion",
        "marginalized", "vulnerable", "social protection", "welfare",
        "beneficiaries", "social inclusion", "discrimination",
    ],
    "Economy": [
        "GDP", "GNI", "income", "revenue", "salary", "wage", "employment",
        "unemployment", "economic", "budget", "investment", "gross product",
        "financial", "insurance", "infrastructure",
    ],
    "Gender": [
        "gender", "women", "men", "female", "male", "sex", "equality",
        "empowerment", "maternal", "reproductive", "domestic violence",
    ],
    "Climate": [
        "climate", "temperature", "flood", "earthquake", "landslide",
        "disaster", "natural hazard", "emission", "carbon", "extreme weather",
        "drought", "precipitation", "rainfall", "greenhouse",
    ],
    "Employment": [
        "employment", "unemployment", "labor", "labour", "job", "workforce",
        "occupation", "profession", "career", "worker", "employee",
        "self-employment", "informal economy",
    ],
}

NUMERICAL_PATTERN = re.compile(
    r"(\d+[.,]?\d*)\s*(?:\-|\sto\s)\s*(\d+[.,]?\d*)\s*"
    r"(?:million|billion|thousand|percent|%|people|inhabitants|USD|EUR|\$|€)?"
)

TIME_SERIES_PATTERN = re.compile(
    r"(?:between|from)\s+(\d{4})\s*(?:and|to)\s+(\d{4})"
    r"|(\d{4})\s*(?:and|to|-)\s*(\d{4})"
    r"|(?:over|during|in)\s+(\d{4})\s*(?:to|and|-)\s*(\d{4})"
)

TIME_SERIES_VALUE_PATTERN = re.compile(
    r"(\d+[.,]?\d*)\s*(million|billion|thousand|percent|%|people|inhabitants|USD|EUR|\$|€)"
)

YEAR_VALID_RANGE = (1900, 2100)


def _is_valid_year(y: int) -> bool:
    return YEAR_VALID_RANGE[0] <= y <= YEAR_VALID_RANGE[1]


def compute_thematic_scores(text: str) -> Dict[str, float]:
    text_lower = text.lower()
    scores = {}
    for theme, keywords in THEME_KEYWORDS.items():
        count = 0
        for kw in keywords:
            count += len(re.findall(r'\b' + re.escape(kw.lower()) + r'\b', text_lower))
        scores[theme] = count
    total = sum(scores.values())
    if total > 0:
        scores = {k: round(v / total * 100, 2) for k, v in scores.items()}
    return scores


def extract_structured_indicators(text: str) -> Dict:
    system_prompt = (
        "You are a data extraction specialist for UN Human Development Reports. "
        "Extract structured data and return ONLY valid JSON."
    )

    chunk = text[:10000] + text[-5000:] if len(text) > 15000 else text

    prompt = (
        "From the following UN Human Development Report text about Serbia, "
        "extract the requested data. Return valid JSON with these exact keys:\n\n"
        '  "key_strengths": List of 5-8 qualitative positive outcomes\n'
        '  "key_challenges": List of 5-8 qualitative systemic risks/vulnerabilities\n'
        '  "core_numerical_indicators": An object with keys:\n'
        '      "HDI value", "HDI rank", "Life expectancy",\n'
        '      "Expected years of schooling", "Mean years of schooling",\n'
        '      "GNI per capita", "Population"\n\n'
        "If a value is not found in the text, use null.\n\n"
        f"TEXT:\n{chunk[:12000]}"
    )

    result_text = llm_complete(
        prompt=prompt,
        system_prompt=system_prompt,
        model=PRIMARY_MODEL,
        temperature=0.05,
        json_mode=True,
    )

    return extract_json_from_llm(result_text)


def extract_time_series_data(text: str) -> List[Dict]:
    records = []

    time_ranges = TIME_SERIES_PATTERN.findall(text)
    for match in time_ranges:
        years = [int(y) for y in match if y and _is_valid_year(int(y))]
        if len(years) >= 2 and years[0] <= years[1]:
            records.append({
                "indicator": "Report time reference",
                "year": years[0],
                "end_year": years[1],
                "value": None,
                "unit": "year range",
            })

    prompt = (
        "From the following text about Serbia's demographic, climate, and "
        "economic trends, extract all quantitative time-series data points. "
        "For each, provide: indicator, year (a single year), value, unit.\n\n"
        "Return JSON as a list of objects with EXACT keys: indicator, year, value, unit.\n"
        "Example: [{\"indicator\": \"Population affected by floods\", \"year\": 2014, \"value\": 1600000, \"unit\": \"people\"}]\n\n"
        "IMPORTANT: Only include entries where you can extract BOTH a year and a numeric value. "
        "Exclude any data points with clearly invalid years (before 1900 or after 2100).\n\n"
        f"TEXT:\n{text[:8000]}"
    )

    result_text = llm_complete(
        prompt=prompt,
        model=PRIMARY_MODEL,
        temperature=0.05,
        json_mode=True,
    )

    llm_data = extract_json_from_llm(result_text)
    raw_entries = []
    if isinstance(llm_data, list):
        raw_entries = llm_data
    elif isinstance(llm_data, dict) and "data" in llm_data:
        raw_entries = llm_data["data"]

    for entry in raw_entries:
        indicator = entry.get("indicator", entry.get("indicator_name", ""))
        year = entry.get("year")
        value = entry.get("value")
        unit = entry.get("unit", "")
        if indicator and year and value is not None:
            try:
                y = int(year)
                if _is_valid_year(y):
                    records.append({
                        "indicator": indicator,
                        "year": y,
                        "value": float(value) if not isinstance(value, (int, float)) else value,
                        "unit": unit,
                    })
            except (ValueError, TypeError):
                pass

    return records


def run_thematic_extraction(text: str, save_output: bool = True) -> Dict:
    print("[thematic_extractor] Computing thematic density scores...")
    thematic_scores = compute_thematic_scores(text)

    print("[thematic_extractor] Extracting structured indicators via LLM...")
    structured = extract_structured_indicators(text)

    print("[thematic_extractor] Extracting time-series data...")
    time_series = extract_time_series_data(text)

    result = {
        "thematic_scores": thematic_scores,
        "key_strengths": structured.get("key_strengths", []),
        "key_challenges": structured.get("key_challenges", []),
        "core_numerical_indicators": structured.get("core_numerical_indicators", {}),
        "time_series_data": time_series,
    }

    if save_output:
        out_path = os.path.join(OUTPUT_DIR, "thematic_extraction.json")
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"[thematic_extractor] Saved to {out_path}")

    return result


if __name__ == "__main__":
    import sys

    txt_path = os.path.join(OUTPUT_DIR, "..", "serbia_hdr_full.txt")
    if not os.path.exists(txt_path):
        from pdf_processor import extract_text_from_pdf

        pdf_path = os.path.join(
            os.path.dirname(__file__),
            "data",
            "nhdrserbia2016engdigitalversion2.pdf",
        )
        if not os.path.exists(pdf_path):
            print(f"ERROR: PDF not found at {pdf_path}")
            sys.exit(1)
        full_text = extract_text_from_pdf(pdf_path)
    else:
        with open(txt_path) as f:
            full_text = f.read()

    result = run_thematic_extraction(full_text, save_output=True)

    print("\n=== THEMATIC SCORES ===")
    for theme, score in sorted(result["thematic_scores"].items(), key=lambda x: -x[1]):
        print(f"  {theme}: {score:.1f}%")

    print(f"\nStrengths: {len(result['key_strengths'])}")
    print(f"Challenges: {len(result['key_challenges'])}")
    print(f"Time-series points: {len(result['time_series_data'])}")
    print("thematic_extractor.py completed successfully.")
