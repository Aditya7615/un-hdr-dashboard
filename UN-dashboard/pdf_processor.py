import json
import os
import re
from typing import Dict, List

from utils import (
    llm_complete,
    extract_json_from_llm,
    clean_pdf_text,
    OUTPUT_DIR,
    PRIMARY_MODEL,
)


CHAPTER_PATTERNS = [
    r"EXECUTIVE SUMMARY",
    r"INTRODUCTION",
    r"CHAPTER\s+\d+",
    r"PART\s+\d+",
    r"CONCEPTUAL FRAMEWORK",
    r"UNDERSTANDING AND REDUCING RISKS",
    r"HOW RESILIENCE CAN BE MEASURED",
    r"HOW RESILIENT ARE SERBIAN COMMUNITIES",
    r"CASE STUDY",
    r"RECOMMENDATIONS",
    r"ANNEX\s+\d+",
    r"REFERENCES",
]


def extract_text_from_pdf(pdf_path: str) -> str:
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    text_parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text.strip():
            text_parts.append(text)
    raw = "\n".join(text_parts)
    return clean_pdf_text(raw)


def segment_by_chapters(text: str) -> Dict[str, str]:
    segments = {}
    lines = text.split("\n")
    current_chapter = "Preamble"
    current_lines = []

    chapter_re = re.compile(
        "|".join(f"({p})" for p in CHAPTER_PATTERNS), re.IGNORECASE
    )

    for line in lines:
        match = chapter_re.search(line.strip().upper())
        if match:
            if current_lines:
                segments[current_chapter] = "\n".join(current_lines).strip()
            current_chapter = line.strip()[:80]
            current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        segments[current_chapter] = "\n".join(current_lines).strip()

    return segments


def extract_key_findings_and_summaries(
    segments: Dict[str, str], full_text: str
) -> Dict:
    system_prompt = (
        "You are an expert analyst extracting structured summaries "
        "from UN Human Development Reports. Always return valid JSON."
    )

    summary_prompt = (
        "Below is the full text of a UN Human Development Report about "
        "social capital and resilience in Serbia.\n\n"
        f"{full_text[:12000]}\n\n"
        "Extract exactly 5-8 key high-level bullet points of overarching "
        "results from this report. Also provide a <100 word summary for "
        "each detected chapter (Executive Summary, Introduction, "
        "Chapter 1, Chapter 2, Recommendations).\n\n"
        "Return JSON with keys:\n"
        '  "key_findings": list of strings,\n'
        '  "chapter_summaries": dict of chapter_name -> summary_string'
    )

    result_text = llm_complete(
        prompt=summary_prompt,
        system_prompt=system_prompt,
        model=PRIMARY_MODEL,
        temperature=0.1,
        json_mode=True,
    )

    result = extract_json_from_llm(result_text)
    return result


def process_pdf_report(
    pdf_path: str = None,
    save_output: bool = True,
) -> Dict:
    if pdf_path is None:
        pdf_path = os.path.join(
            os.path.dirname(__file__),
            "data",
            "nhdrserbia2016engdigitalversion2.pdf",
        )

    print(f"[pdf_processor] Extracting text from: {pdf_path}")
    full_text = extract_text_from_pdf(pdf_path)

    print(f"[pdf_processor] Text length: {len(full_text)} chars")
    print(f"[pdf_processor] Segmenting by chapters...")
    segments = segment_by_chapters(full_text)

    print(f"[pdf_processor] Found {len(segments)} segments")
    for ch_name, ch_text in segments.items():
        print(f"  - '{ch_name[:60]}': {len(ch_text)} chars")

    print(f"[pdf_processor] Extracting key findings and summaries via LLM...")
    extraction = extract_key_findings_and_summaries(segments, full_text)

    result = {
        "full_text_length": len(full_text),
        "num_segments": len(segments),
        "segments": {k: v[:500] for k, v in segments.items()},
        "key_findings": extraction.get("key_findings", []),
        "chapter_summaries": extraction.get("chapter_summaries", {}),
    }

    if save_output:
        out_path = os.path.join(OUTPUT_DIR, "pdf_summary.json")
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"[pdf_processor] Saved summary to {out_path}")

    return result


def process_country_assignments(
    pdf_path: str = None,
    save_output: bool = True,
) -> List[Dict]:
    if pdf_path is None:
        pdf_path = os.path.join(
            os.path.dirname(__file__),
            "data",
            "assignment_1_country_assignment.pdf",
        )

    print(f"[pdf_processor] Extracting country assignments from: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)

    records = []
    pattern = re.compile(
        r"([A-Za-z\s\-\.\,\']+?)\s+(\d{6})([A-Za-z\s]+?)(\d{4}(?:/\d{2,4})?)?(?:\s|$)"
    )
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        match = pattern.search(line)
        if match:
            name = match.group(1).strip()
            student_id = match.group(2).strip()
            country = match.group(3).strip()
            year = match.group(4).strip() if match.group(4) else ""
            if name and student_id and country:
                records.append({
                    "student_name": name,
                    "student_id": student_id,
                    "country": country,
                    "year": year,
                })

    result = {"total_students": len(records), "assignments": records}

    if save_output:
        out_path = os.path.join(OUTPUT_DIR, "country_assignments.json")
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"[pdf_processor] Saved {len(records)} assignments to {out_path}")

    return records


if __name__ == "__main__":
    import sys

    base = os.path.join(os.path.dirname(__file__), "data")
    report_pdf = os.path.join(base, "nhdrserbia2016engdigitalversion2.pdf")
    assign_pdf = os.path.join(base, "assignment_1_country_assignment.pdf")

    if not os.path.exists(report_pdf):
        print(f"ERROR: Report PDF not found at {report_pdf}")
        sys.exit(1)

    summary = process_pdf_report(report_pdf, save_output=True)

    if os.path.exists(assign_pdf):
        assignments = process_country_assignments(assign_pdf, save_output=True)
    else:
        print("Country assignment PDF not found, skipping.")
        assignments = []

    print("\n=== KEY FINDINGS ===")
    for i, f in enumerate(summary.get("key_findings", []), 1):
        print(f"  {i}. {f}")

    print(f"\nTotal country assignments: {len(assignments)}")
    print("pdf_processor.py completed successfully.")
