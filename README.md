# PKD Literature Search

Automated tool that searches **PubMed**, **bioRxiv**, and **medRxiv** for polycystic kidney disease (PKD) publications and generates downloadable Excel and PDF reports.

Available as both a **Streamlit web app** and a **command-line script**.

## Features

- **Multi-database search** — queries PubMed, bioRxiv, and medRxiv in a single run
- **Automatic categorization** — papers sorted into Genetics, Therapeutics, Metabolism, Cross-species, Datasets, Clinical, Pathophysiology, and Other
- **Excel report** — structured spreadsheet with summary, last author, journal, key findings, and clickable links
- **PDF report** — formatted document with search summary, notable findings by category, and complete citation list
- **Deduplication** — removes duplicates across databases by DOI and title
- **Retry logic** — robust error handling with automatic retries for API failures

## Quick Start

### Streamlit Web App

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501, pick your date range, and click **Run Search**.

### Command Line

```bash
# Search last 7 days (default)
python pkd_literature_search.py

# Search a specific date range
python pkd_literature_search.py --start 2026-02-01 --end 2026-02-08

# Specify output directory
python pkd_literature_search.py --start 2026-02-01 --end 2026-02-08 --output ./reports
```

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`:

```
streamlit>=1.30.0
requests>=2.28.0
openpyxl>=3.1.0
reportlab>=4.0.0
pandas>=1.5.0
```

Install with:

```bash
pip install -r requirements.txt
```

## Output Files

### Excel (.xlsx)

| Column | Content |
|--------|---------|
| D | Summary (< 8 words) |
| E | Last author's last name |
| F | Journal |
| G | Key findings (< 20 words) |
| J | Clickable DOI or PubMed link |

### PDF

1. **Search Summary** — total papers, database breakdown, date range
2. **Notable Findings** — top papers organized by category (Metabolism, Therapeutics, Cross-species, Datasets)
3. **Complete Paper List** — full citations with clickable links

Files are named using the end date: `YYYYMMDD-PKD-Literature-Data.xlsx` and `YYYYMMDD-PKD-Literature-Summary.pdf`.

## Search Query

The tool searches for papers matching:

> "polycystic kidney" OR "polycystic kidney disease" OR "ADPKD" OR "ARPKD" OR PKD1 OR PKD2

For bioRxiv/medRxiv, additional keyword filtering is applied including: polycystin, fibrocystin, cystogenesis, PKHD1, kidney cyst, renal cyst, and related terms.

## Project Structure

```
PKDLitSearch/
├── app.py                      # Streamlit web app
├── pkd_literature_search.py    # Core search class (CLI + library)
├── requirements.txt            # Python dependencies
├── LICENSE                     # GPL-3.0
└── README.md
```

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
