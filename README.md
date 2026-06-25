# KRAZ Recruitment Intelligence Platform

An end-to-end recruitment intelligence platform built with Python and Streamlit.

## Overview

This project automates the extraction, cleaning, filtering, ranking, and analysis of recruitment agencies listed in the Polish KRAZ registry.

The platform identifies agencies that provide services for foreign workers, prioritizes high-value leads, and generates outreach-ready datasets through a fully automated pipeline.

## Features

* Automated KRAZ registry extraction
* Data normalization and validation
* Foreign-worker agency filtering
* Lead scoring and prioritization
* Outreach dataset generation
* Interactive Streamlit dashboard
* Pipeline automation
* Logging and monitoring

## Technology Stack

* Python
* Pandas
* Requests
* OpenPyXL
* Streamlit
* Git & GitHub

## Pipeline Workflow

1. Extract registry records
2. Normalize raw data
3. Filter agencies serving foreign workers
4. Rank and score leads
5. Generate outreach-ready datasets
6. Visualize insights through Streamlit

## Dashboard

The Streamlit dashboard provides:

* Lead statistics
* Agency search
* Pipeline controls
* Data refresh functionality
* Live status monitoring

## Project Structure

extractor.py → Data extraction

normalize.py → Data cleaning

check_foreigners.py → Foreign-worker filtering

rank_leads_v2.py → Lead scoring

prepare_outreach.py → Outreach dataset generation

dashboard.py → Streamlit dashboard

run_pipeline.py → Full pipeline automation

## Author

Temple Tochukwu
