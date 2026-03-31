import os
import pandas as pd

AB_RESULTS_PATH = "outputs/reports/ab_test_results_summary.csv"
ML_METRICS_PATH = "outputs/reports/ml_model_metrics.csv"
TOP_SEGMENTS_PATH = "outputs/reports/top_segment_uplift_table.csv"
OUTPUT_DIR = "outputs/reports"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "experiment_summary.txt")


def load_csv_safe(path):
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


def format_metric(value, is_percent=False):
    if pd.isna(value):
        return "N/A"
    if is_percent:
        return f"{value * 100:.2f}%"
    return f"{value:.4f}"


def build_summary(ab_df, ml_df, seg_df):
    lines = []
    lines.append("AI-Powered Experiment Summary")
    lines.append("=" * 40)
    lines.append("")

    # A/B test section
    lines.append("1. A/B Test Results")
    if ab_df is not None and not ab_df.empty:
        for _, row in ab_df.iterrows():
            metric = row["metric"]
            a = row["variant_a"]
            b = row["variant_b"]
            diff = row["absolute_difference"]
            p = row["p_value"]

            is_percent_metric = metric in ["signup_rate", "watch_start_rate"]

            lines.append(f"- {metric}:")
            lines.append(
                f"  - Variant A: {format_metric(a, is_percent=is_percent_metric)}")
            lines.append(
                f"  - Variant B: {format_metric(b, is_percent=is_percent_metric)}")
            lines.append(
                f"  - Difference: {format_metric(diff, is_percent=is_percent_metric)}")
            lines.append(f"  - P-value: {format_metric(p)}")

            if pd.notna(p):
                if p < 0.05:
                    lines.append(
                        "  - Interpretation: statistically significant difference detected.")
                else:
                    lines.append(
                        "  - Interpretation: no statistically significant difference detected.")
    else:
        lines.append("- A/B test results file not found.")

    lines.append("")

    # ML section
    lines.append("2. ML Model Performance")
    if ml_df is not None and not ml_df.empty:
        for _, row in ml_df.iterrows():
            lines.append(f"- {row['metric']}: {row['value']:.4f}")
    else:
        lines.append("- ML metrics file not found.")

    lines.append("")

    # Segment section
    lines.append("3. Top Segment Insights")
    if seg_df is not None and not seg_df.empty:
        top_rows = seg_df.head(5)
        for i, (_, row) in enumerate(top_rows.iterrows(), start=1):
            lines.append(
                f"- Top Segment {i}: device={row['device_type']}, "
                f"source={row['traffic_source']}, "
                f"is_new_user={row['is_new_user']}, "
                f"sessions={int(row['sessions'])}, "
                f"absolute_lift={row['absolute_lift']:.4f}, "
                f"relative_lift_pct={row['relative_lift_pct']:.2f}%"
            )
    else:
        lines.append("- Segment uplift file not found.")

    lines.append("")

    # Executive summary
    lines.append("4. Executive Recommendation")
    if ab_df is not None and not ab_df.empty:
        signup_row = ab_df[ab_df["metric"] == "signup_rate"]

        if not signup_row.empty:
            p_value = signup_row["p_value"].iloc[0]
            diff = signup_row["absolute_difference"].iloc[0]

            if p_value < 0.05 and diff > 0:
                lines.append(
                    "- Variant B improved the primary conversion metric with statistical significance. "
                    "This suggests Variant B is a strong candidate for rollout, with additional monitoring by segment."
                )
            elif diff > 0:
                lines.append(
                    "- Variant B showed positive lift, but significance may be limited. "
                    "Consider further validation or larger sample sizes before rollout."
                )
            else:
                lines.append(
                    "- Variant B did not clearly outperform Variant A on the primary metric. "
                    "A broader redesign or new hypothesis may be needed."
                )
        else:
            lines.append("- Primary metric row not found in A/B results.")
    else:
        lines.append(
            "- Unable to generate rollout recommendation because A/B results are missing.")

    lines.append("")
    lines.append("5. Suggested Next Experiments")
    lines.append(
        "- Test personalized content ranking for high-response user segments.")
    lines.append(
        "- Create segment-specific homepage layouts for new versus returning users.")
    lines.append("- Evaluate different CTA messaging by traffic source.")
    lines.append(
        "- Test a more aggressive recommendation design for high-engagement cohorts.")

    return "\n".join(lines)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    ab_df = load_csv_safe(AB_RESULTS_PATH)
    ml_df = load_csv_safe(ML_METRICS_PATH)
    seg_df = load_csv_safe(TOP_SEGMENTS_PATH)

    summary_text = build_summary(ab_df, ml_df, seg_df)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(summary_text)

    print("Summary report created successfully.")
    print(f"Saved to: {OUTPUT_PATH}")
    print("\n")
    print(summary_text)


if __name__ == "__main__":
    main()
