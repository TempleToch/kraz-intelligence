import streamlit as st
import pandas as pd
import subprocess
import time

from pathlib import Path
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="KRAZ Recruitment Intelligence Platform",
    layout="wide"
)

st.title("KRAZ Recruitment Intelligence Platform")
st.caption(
    "Automated recruitment agency extraction, filtering, ranking and outreach intelligence system."
)

DATA = Path("data")

# =====================================
# HELPERS
# =====================================

def run_script(script_name):

    result = subprocess.run(
        ["python", script_name],
        capture_output=True,
        text=True
    )

    return (
        result.returncode,
        result.stdout,
        result.stderr
    )


@st.cache_data(ttl=300)
def load_data():

    ranked = pd.read_excel(
        DATA / "demo_ranked_leads.xlsx",
        engine="openpyxl"
    )

    outreach = pd.read_excel(
        DATA / "demo_outreach.xlsx",
        engine="openpyxl"
    )

    foreigners = pd.read_excel(
        DATA / "demo_foreigners.xlsx",
        engine="openpyxl"
    )

    return ranked, outreach, foreigners

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("Pipeline Controls")

if st.sidebar.button("Run Full Pipeline"):

    with st.spinner("Running pipeline..."):

        code, out, err = run_script(
            "run_pipeline.py"
        )

    if code == 0:

        st.sidebar.success(
            "Pipeline completed successfully"
        )

        with st.expander(
            "Pipeline Output"
        ):
            st.text(out)

        st.cache_data.clear()
        st.rerun()

    else:

        st.sidebar.error(
            "Pipeline failed"
        )

        with st.expander(
            "Error Details"
        ):
            st.text(err)


st.sidebar.markdown("---")

if st.sidebar.button("Extractor"):

    code, out, err = run_script(
        "extractor.py"
    )

    if code == 0:
        st.sidebar.success(
            "Extraction completed"
        )
        st.cache_data.clear()

    else:
        st.sidebar.error(err)


if st.sidebar.button("Normalize"):

    code, out, err = run_script(
        "normalize.py"
    )

    if code == 0:
        st.sidebar.success(
            "Normalization completed"
        )
        st.cache_data.clear()

    else:
        st.sidebar.error(err)


if st.sidebar.button("Foreigners Filter"):

    code, out, err = run_script(
        "check_foreigners.py"
    )

    if code == 0:
        st.sidebar.success(
            "Filtering completed"
        )
        st.cache_data.clear()

    else:
        st.sidebar.error(err)


if st.sidebar.button("Rank Leads"):

    code, out, err = run_script(
        "rank_leads_v2.py"
    )

    if code == 0:
        st.sidebar.success(
            "Lead ranking completed"
        )
        st.cache_data.clear()

    else:
        st.sidebar.error(err)


if st.sidebar.button("Prepare Outreach"):

    code, out, err = run_script(
        "prepare_outreach.py"
    )

    if code == 0:
        st.sidebar.success(
            "Outreach file created"
        )
        st.cache_data.clear()

    else:
        st.sidebar.error(err)


# =====================================
# FILE STATUS
# =====================================

st.sidebar.markdown("---")
st.sidebar.subheader("Pipeline Status")

required_files = [
    "raw_kraz.xlsx",
    "raw_kraz_clean.xlsx",
    "foreigners_agencies.xlsx",
    "foreigners_ranked_leads_v2.xlsx",
    "outreach_ready_leads.xlsx"
]

for file in required_files:

    path = DATA / file

    if path.exists():
        st.sidebar.success(file)
    else:
        st.sidebar.error(file)


# =====================================
# MAIN DASHBOARD
# =====================================

st.title(
    "KRAZ Recruitment Agency Intelligence Dashboard"
)

start = time.time()

try:

    ranked, outreach, foreigners = load_data()

except Exception as e:

    st.error(
        f"Could not load data files: {e}"
    )

    st.stop()

elapsed = round(
    time.time() - start,
    2
)

st.caption(
    f"Data loaded in {elapsed} seconds"
)

# =====================================
# METRICS
# =====================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Foreigner Agencies",
        len(foreigners)
    )

with col2:
    st.metric(
        "Ranked Leads",
        len(ranked)
    )

with col3:
    st.metric(
        "Outreach Ready",
        len(outreach)
    )
st.divider()

st.subheader("Visual Analytics")

city_counts = (
    foreigners["miejscowosc"]
    .value_counts()
    .head(10)
)

st.subheader("Top 10 Cities")

st.bar_chart(city_counts)

if "wojewodztwo" in foreigners.columns:

    region_counts = (
        foreigners["wojewodztwo"]
        .value_counts()
        .head(10)
    )

    st.subheader("Top Regions")

    st.bar_chart(region_counts)

    st.subheader("Lead Dataset Distribution")

summary = pd.DataFrame({
    "Dataset": [
        "Foreigner Agencies",
        "Ranked Leads",
        "Outreach Ready"
    ],
    "Count": [
        len(foreigners),
        len(ranked),
        len(outreach)
    ]
})

st.bar_chart(
    summary.set_index("Dataset")
)


# =====================================
# SEARCH
# =====================================

st.divider()

st.subheader(
    "Search Agencies"
)

query = st.text_input(
    "Search by company, email, city, phone or NIP"
)

if query:

    results = ranked[
        ranked.astype(str)
        .apply(
            lambda x: x.str.contains(
                query,
                case=False,
                na=False
            )
        )
        .any(axis=1)
    ]

    st.write(
        f"{len(results)} result(s)"
    )

    st.dataframe(
        results,
        use_container_width=True
    )

# =====================================
# TOP LEADS
# =====================================

st.divider()

st.subheader(
    "Top Ranked Leads"
)

st.dataframe(
    ranked.head(100),
    use_container_width=True,
    height=600
)

# =====================================
# DOWNLOADS
# =====================================

st.divider()

st.subheader(
    "Downloads"
)

with open(
    DATA / "demo_ranked_leads.xlsx",
    "rb"
) as f:

    st.download_button(
        "Download Demo Ranked Leads",
        f,
        file_name="demo_ranked_leads.xlsx"
    )

with open(
    DATA / "demo_outreach.xlsx",
    "rb"
) as f:

    st.download_button(
        "Download Demo Outreach Leads",
        f,
        file_name="demo_outreach.xlsx"
    )


# =====================================
# LAST UPDATE
# =====================================

st.divider()

file_time = datetime.fromtimestamp(
    (DATA / "demo_ranked_leads.xlsx").stat().st_mtime
)

st.caption(
    f"Last Pipeline Update: {file_time}"
)

if st.button("Refresh Dashboard"):

    st.cache_data.clear()

    st.rerun()