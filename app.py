import os
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="A/B Testing AI Dashboard", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "data" / "processed" / "experiment_data_clean.csv"
AB_RESULTS_PATH = BASE_DIR / "outputs" / \
    "reports" / "ab_test_results_summary.csv"
ML_METRICS_PATH = BASE_DIR / "outputs" / "reports" / "ml_model_metrics.csv"
TOP_SEGMENTS_PATH = BASE_DIR / "outputs" / \
    "reports" / "top_segment_uplift_table.csv"
SUMMARY_PATH = BASE_DIR / "outputs" / "reports" / "experiment_summary.txt"


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)


@st.cache_data
def load_optional_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


@st.cache_data
def load_summary(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "Summary file not found."


df = load_data()
ab_results = load_optional_csv(AB_RESULTS_PATH)
ml_metrics = load_optional_csv(ML_METRICS_PATH)
top_segments = load_optional_csv(TOP_SEGMENTS_PATH)
summary_text = load_summary(SUMMARY_PATH)

st.title("AI-Powered A/B Testing Dashboard")
st.write("Netflix-inspired experimentation, ML analysis, and AI-generated reporting")

st.sidebar.header("Filters")

selected_device = st.sidebar.selectbox(
    "Device Type",
    options=["All"] + sorted(df["device_type"].dropna().unique().tolist())
)

selected_source = st.sidebar.selectbox(
    "Traffic Source",
    options=["All"] + sorted(df["traffic_source"].dropna().unique().tolist())
)

selected_user_type = st.sidebar.selectbox(
    "User Type",
    options=["All", "New", "Returning"]
)

filtered_df = df.copy()

if selected_device != "All":
    filtered_df = filtered_df[filtered_df["device_type"] == selected_device]

if selected_source != "All":
    filtered_df = filtered_df[filtered_df["traffic_source"] == selected_source]

if selected_user_type == "New":
    filtered_df = filtered_df[filtered_df["is_new_user"] == 1]
elif selected_user_type == "Returning":
    filtered_df = filtered_df[filtered_df["is_new_user"] == 0]

st.subheader("Overview")

total_sessions = len(filtered_df)
signup_rate = filtered_df["signed_up"].mean()
watch_rate = filtered_df["watch_started"].mean()
avg_duration = filtered_df["session_duration_sec"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Sessions", f"{total_sessions:,}")
col2.metric("Signup Rate", f"{signup_rate:.2%}")
col3.metric("Watch Start Rate", f"{watch_rate:.2%}")
col4.metric("Avg Session Duration", f"{avg_duration:.1f} sec")

st.divider()

st.subheader("Experiment KPI Comparison")

variant_summary = filtered_df.groupby("variant").agg(
    sessions=("session_id", "count"),
    signup_rate=("signed_up", "mean"),
    watch_start_rate=("watch_started", "mean"),
    click_rate=("clicked_recommendation", "mean"),
    avg_session_duration=("session_duration_sec", "mean"),
    retention_rate=("retained_7d", "mean")
).reset_index()

st.dataframe(variant_summary, use_container_width=True)

st.bar_chart(
    variant_summary.set_index(
        "variant")[["signup_rate", "watch_start_rate", "retention_rate"]]
)

st.divider()

st.subheader("Segment Performance")

segment_summary = filtered_df.groupby(["device_type", "variant"]).agg(
    signup_rate=("signed_up", "mean"),
    watch_start_rate=("watch_started", "mean"),
    avg_session_duration=("session_duration_sec", "mean")
).reset_index()

st.dataframe(segment_summary, use_container_width=True)

pivot_signup = segment_summary.pivot(
    index="device_type", columns="variant", values="signup_rate")
st.bar_chart(pivot_signup)

st.divider()

st.subheader("Traffic Source Performance")

source_summary = filtered_df.groupby(["traffic_source", "variant"]).agg(
    signup_rate=("signed_up", "mean"),
    watch_start_rate=("watch_started", "mean")
).reset_index()

st.dataframe(source_summary, use_container_width=True)

pivot_source = source_summary.pivot(
    index="traffic_source", columns="variant", values="signup_rate")
st.bar_chart(pivot_source)

st.divider()

st.subheader("A/B Test Results Summary")
if ab_results is not None:
    st.dataframe(ab_results, use_container_width=True)
else:
    st.warning("A/B results file not found.")

st.subheader("ML Model Metrics")
if ml_metrics is not None:
    st.dataframe(ml_metrics, use_container_width=True)
else:
    st.warning("ML metrics file not found.")

st.subheader("Top Uplift Segments")
if top_segments is not None:
    st.dataframe(top_segments.head(10), use_container_width=True)
else:
    st.warning("Top segment uplift file not found.")

st.divider()

st.subheader("AI-Generated Experiment Summary")
st.text(summary_text)
