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
    page_title="KRAZ Lead Intelligence",
    layout="wide"
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
        DATA / "foreigners_ranked_leads_v2.xlsx",
        engine="openpyxl"
    )

    outreach = pd.read_excel(
        DATA / "outreach_ready_leads.xlsx",
        engine="openpyxl"
    )

    foreigners = pd.read_excel(
        DATA / "foreigners_agencies.xlsx",
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
    DATA / "foreigners_ranked_leads_v2.xlsx",
    "rb"
) as f:

    st.download_button(
        "Download Ranked Leads",
        f,
        file_name="foreigners_ranked_leads_v2.xlsx"
    )

with open(
    DATA / "outreach_ready_leads.xlsx",
    "rb"
) as f:

    st.download_button(
        "Download Outreach Leads",
        f,
        file_name="outreach_ready_leads.xlsx"
    )

# =====================================
# LAST UPDATE
# =====================================

st.divider()

file_time = datetime.fromtimestamp(
    (
        DATA /
        "foreigners_ranked_leads_v2.xlsx"
    ).stat().st_mtime
)

st.caption(
    f"Last Pipeline Update: {file_time}"
)

if st.button("Refresh Dashboard"):

    st.cache_data.clear()

    st.rerun()