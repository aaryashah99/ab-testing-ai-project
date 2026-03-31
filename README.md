# AI-Powered A/B Testing Platform for Consumer Web Products

A Netflix-inspired experimentation analytics project that combines A/B testing, SQL, machine learning, and AI-generated summaries to evaluate how product changes affect user conversion and engagement.

## Project Overview

Consumer web platforms frequently test changes to landing pages, recommendation layouts, and user flows. This project simulates a real-world experimentation workflow by generating event-level product data, running statistical A/B tests, analyzing segment-level uplift, training an ML conversion model, and generating AI-style executive summaries.

## Business Problem

Experimentation teams need to answer one core question:

**Did this product change move the needle?**

This project was designed to evaluate that question using:
- controlled A/B test comparisons
- statistical significance testing
- segment-level performance analysis
- predictive ML modeling
- automated reporting

## Objectives

- Measure the impact of experiment variants on signup conversion and engagement
- Identify which user segments respond most strongly to treatment
- Predict conversion using user behavior and experiment assignment
- Generate stakeholder-ready summaries and recommended next experiments
- Build a dashboard for interactive experiment review

## Features

- Simulates experiment data for consumer web product testing
- Runs statistical A/B test analysis on conversion and engagement outcomes
- Analyzes uplift across traffic sources, devices, and behavioral segments
- Trains a machine learning model to predict conversion likelihood
- Generates AI-style executive summaries of experiment performance
- Provides a Streamlit dashboard for interactive review

## Tech Stack

- **Python**
- **pandas**
- **NumPy**
- **SciPy**
- **statsmodels**
- **scikit-learn**
- **DuckDB / SQL**
- **Streamlit**
- **Matplotlib**

## Project Structure

```text
ab-testing-ai-project/
├── notebooks/
│   ├── outputs/
│   │   └── charts/
│   ├── 01_data_generation_and_cleaning.ipynb
│   ├── 02_ab_test_analysis.ipynb
│   └── 03_ml_segmentation_prediction.ipynb
├── sql/
│   └── metric_queries.sql
├── src/
│   ├── ab_test.py
│   ├── generate_data.py
│   ├── llm_summary.py
│   ├── ml_model.py
│   ├── preprocess.py
│   └── run_sql_analysis.py
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
