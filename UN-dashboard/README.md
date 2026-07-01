# UN HDR Serbia 2016 — Interactive Dashboard

An interactive **Streamlit dashboard** exploring the **National Human Development Report: Serbia 2016 — Social Capital: The Invisible Face of Resilience**. Extracts thematic patterns, time-series trends, I-distance rankings, and resilience capital scores from the UN report using keyword analysis, LLM extraction, and the Ivanović I-distance method.

## Features

- **Thematic Density** — Bar/pie/treemap of keyword frequency across 7 themes (Education, Health, Inequality, Economy, Gender, Climate, Employment)
- **Cross-Model Validation** — Compare extracted indicators against simulated runs with grouped bar and scatter views
- **Time Trends** — Historical line/area/bar charts for floods, HDI, economic damage, and temperature anomalies
- **Resilience Capitals** — Radar chart of 5 capitals (Natural, Physical, Economic, Human, Social/Institutional) with municipality overlay
- **Correlation Matrix** — Pearson correlation heatmap of indicators + I-distance distribution histogram
- **Country Explorer** — Browse 117 student country assignments extracted from the PDF

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Project Structure

```
UN-dashboard/
├── app.py                      # Main Streamlit dashboard (6 tabs)
├── pipeline.py                 # End-to-end extraction pipeline
├── pdf_processor.py            # PDF text extraction & chapter segmentation
├── thematic_extractor.py       # Keyword scoring + LLM-based extraction
├── idistance_engine.py         # Ivanović I-distance ranking engine
├── evaluation_framework.py     # Quality & consistency evaluation
├── utils.py                    # LLM client, mock mode, helpers
├── requirements.txt            # Python dependencies
├── .streamlit/config.toml      # Streamlit theme & server config
├── data/
│   ├── nhdrserbia2016engdigitalversion2.pdf   # Full UN report
│   ├── assignment_1_country_assignment.pdf    # Student assignments
│   └── output/                                 # Generated JSON data
│       ├── thematic_extraction.json
│       ├── idistance_results.json
│       ├── evaluation_report.json
│       ├── pdf_summary.json
│       └── country_assignments.json
└── README.md
```

## Pipeline

Run the full pipeline to regenerate extracted data:

```bash
python pipeline.py --mock
```

Uses mock LLM mode by default. Set `GROQ_API_KEY` in `.env` for real LLM extraction.

## Deployment

Deploy on **Streamlit Cloud** (free):

1. Push this directory to a GitHub repo
2. Go to https://streamlit.io/cloud
3. New app → select repo → main file: `UN-dashboard/app.py`
4. Deploy

No API keys needed — dashboard works with built-in fallback data.

## Data Source

United Nations Development Programme (UNDP). *National Human Development Report: Serbia 2016 — Social Capital: The Invisible Face of Resilience*. Belgrade, 2016.
