"""
PKD Literature Search -- Streamlit App
=======================================
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta
from pkd_literature_search import PKDLiteratureSearch

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="PKD Literature Search",
    page_icon="🔬",
    layout="wide",
)

st.title("PKD Literature Search")
st.markdown(
    "Search **PubMed**, **bioRxiv**, and **medRxiv** for recent polycystic kidney "
    "disease publications and download the results as Excel or PDF."
)

# ---------------------------------------------------------------------------
# Sidebar -- date inputs
# ---------------------------------------------------------------------------
st.sidebar.header("Search Parameters")

default_end = date.today()
default_start = default_end - timedelta(days=7)

start_date = st.sidebar.date_input("Start date", value=default_start)
end_date = st.sidebar.date_input("End date", value=default_end)

if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")

run_search = st.sidebar.button("Run Search", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------

if run_search and start_date <= end_date:
    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    searcher = PKDLiteratureSearch(start_str, end_str)

    # Run the search with a spinner
    with st.spinner("Searching PubMed, bioRxiv, and medRxiv ..."):
        all_papers, pubmed, biorxiv, medrxiv, categories = searcher.search_all()

    # Store results in session state so they survive reruns
    st.session_state["results"] = {
        "all_papers": all_papers,
        "pubmed": pubmed,
        "biorxiv": biorxiv,
        "medrxiv": medrxiv,
        "categories": categories,
        "searcher": searcher,
        "start_str": start_str,
        "end_str": end_str,
    }

# ---------------------------------------------------------------------------
# Display results (if available)
# ---------------------------------------------------------------------------

if "results" in st.session_state:
    res = st.session_state["results"]
    all_papers = res["all_papers"]
    pubmed = res["pubmed"]
    biorxiv = res["biorxiv"]
    medrxiv = res["medrxiv"]
    categories = res["categories"]
    searcher = res["searcher"]

    # Summary metrics
    st.subheader("Search Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Papers", len(all_papers))
    col2.metric("PubMed", len(pubmed))
    col3.metric("bioRxiv", len(biorxiv))
    col4.metric("medRxiv", len(medrxiv))

    # Category breakdown
    st.subheader("Categories")
    cat_cols = st.columns(len(categories))
    labels = {
        "genetics": "Genetics",
        "therapeutics": "Therapeutics",
        "metabolism": "Metabolism",
        "pathophysiology": "Pathophysiology",
        "clinical": "Clinical",
        "cross_species": "Cross-species",
        "dataset": "Datasets",
        "other": "Other",
    }
    for col, (key, label) in zip(cat_cols, labels.items()):
        col.metric(label, len(categories[key]))

    # Results table
    st.subheader(f"Results ({len(all_papers)} papers)")

    if all_papers:
        df = pd.DataFrame(all_papers)

        # Build a clickable link column
        def _make_link(row):
            doi = row.get("doi", "")
            pmid = row.get("pmid", "")
            if doi:
                return f"https://doi.org/{doi}"
            if pmid:
                return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            return ""

        df["link"] = df.apply(_make_link, axis=1)

        display_cols = ["title", "authors", "journal", "year", "source", "link"]
        display_cols = [c for c in display_cols if c in df.columns]

        st.dataframe(
            df[display_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                "title": st.column_config.TextColumn("Title", width="large"),
                "authors": st.column_config.TextColumn("Authors", width="medium"),
                "journal": st.column_config.TextColumn("Journal"),
                "year": st.column_config.TextColumn("Year", width="small"),
                "source": st.column_config.TextColumn("Source", width="small"),
                "link": st.column_config.LinkColumn("Link", width="medium"),
            },
        )

        # Downloads
        st.subheader("Download Reports")
        dl_col1, dl_col2 = st.columns(2)

        end_fmt = res["end_str"].replace("-", "")

        with dl_col1:
            excel_bytes = searcher.create_excel_bytes(all_papers)
            st.download_button(
                label="Download Excel",
                data=excel_bytes,
                file_name=f"{end_fmt}-PKD-Literature-Data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        with dl_col2:
            pdf_bytes = searcher.create_pdf_bytes(
                all_papers,
                categories,
                pubmed_count=len(pubmed),
                biorxiv_count=len(biorxiv),
                medrxiv_count=len(medrxiv),
            )
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"{end_fmt}-PKD-Literature-Summary.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    else:
        st.info("No papers found for this date range.")
else:
    st.info("Select a date range in the sidebar and click **Run Search** to begin.")
