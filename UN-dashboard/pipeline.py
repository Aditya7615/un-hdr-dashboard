#!/usr/bin/env python3
"""
Integrated pipeline runner: PDF extraction -> Thematic analysis ->
I-distance engine -> Evaluation -> Dashboard data generation.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from utils import OUTPUT_DIR
from pdf_processor import process_pdf_report, process_country_assignments, extract_text_from_pdf
from thematic_extractor import run_thematic_extraction
from idistance_engine import build_idistance_pipeline, create_sample_dataset
from evaluation_framework import run_evaluation_pipeline


def run_pipeline(
    report_pdf: str,
    assign_pdf: str = None,
    mock_llm: bool = False,
    save: bool = True,
):
    if mock_llm:
        os.environ["LLM_MOCK_MODE"] = "1"
        print("[pipeline] MOCK LLM MODE ENABLED")

    print("=" * 60)
    print("UN HDR SERBIA 2016 — FULL ANALYSIS PIPELINE")
    print("=" * 60)

    print("\n[1/5] PDF Processing & Summary Engine")
    summary = process_pdf_report(report_pdf, save_output=save)

    print(f"\n  Key Findings: {len(summary.get('key_findings', []))}")
    print(f"  Chapters: {len(summary.get('chapter_summaries', {}))}")

    if assign_pdf and os.path.exists(assign_pdf):
        print("\n[1b/5] Country Assignments")
        assignments = process_country_assignments(assign_pdf, save_output=save)
        print(f"  Students assigned: {len(assignments)}")

    print("\n[2/5] Thematic & Structured Indicator Extraction")
    full_text = extract_text_from_pdf(report_pdf)
    thematic = run_thematic_extraction(full_text, save_output=save)
    print(f"  Themes tracked: {len(thematic.get('thematic_scores', {}))}")
    print(f"  Time-series points: {len(thematic.get('time_series_data', []))}")

    print("\n[3/5] Ivanović I-Distance Engine")
    sample_df = create_sample_dataset()
    idist = build_idistance_pipeline(
        df=sample_df,
        entity_col="entity",
        negative_indicators=["unemployment_rate", "flood_risk_score"],
        save_output=save,
    )
    print(f"  Entities ranked: {idist['entity_count']}")
    print(f"  Top entity: {idist['entity_scores'][0]['entity']}")

    print("\n[4/5] Evaluation Framework")
    eval_report = run_evaluation_pipeline(
        thematic_data=thematic,
        raw_text_chunks=[full_text[:3000]],
        n_runs=2,
        save_output=save,
    )
    print(f"  Overall Quality: {eval_report['overall_quality_score']:.1f}%")

    print("\n[5/5] Dashboard Data Ready")
    output_files = os.listdir(OUTPUT_DIR)
    for f in sorted(output_files):
        fpath = os.path.join(OUTPUT_DIR, f)
        size = os.path.getsize(fpath)
        print(f"  {f} ({size:,} bytes)")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print(f"To launch dashboard: streamlit run {os.path.join(os.path.dirname(__file__), 'app.py')}")
    print("=" * 60)

    return {
        "summary": summary,
        "thematic": thematic,
        "idistance": idist,
        "evaluation": eval_report,
    }


if __name__ == "__main__":
    import argparse

    base_dir = os.path.join(os.path.dirname(__file__), "data")
    default_report = os.path.join(base_dir, "nhdrserbia2016engdigitalversion2.pdf")
    default_assign = os.path.join(base_dir, "assignment_1_country_assignment.pdf")

    parser = argparse.ArgumentParser(description="UN HDR Serbia 2016 Pipeline")
    parser.add_argument("--report-pdf", default=default_report)
    parser.add_argument("--assign-pdf", default=default_assign)
    parser.add_argument("--mock", action="store_true", help="Use mock LLM")
    parser.add_argument("--no-save", action="store_true", help="Skip saving output")
    args = parser.parse_args()

    if not os.path.exists(args.report_pdf):
        print(f"ERROR: Report PDF not found at {args.report_pdf}")
        sys.exit(1)

    run_pipeline(
        report_pdf=args.report_pdf,
        assign_pdf=args.assign_pdf if os.path.exists(args.assign_pdf) else None,
        mock_llm=args.mock,
        save=not args.no_save,
    )
