import os
import pandas as pd

INPUT_PATH = "data/raw/experiment_data.csv"
OUTPUT_DIR = "data/processed"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "experiment_data_clean.csv")


def main():
    # Load data
    df = pd.read_csv(INPUT_PATH)

    print("Raw shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    # Standardize column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Remove duplicate rows
    before_dupes = df.shape[0]
    df = df.drop_duplicates()
    after_dupes = df.shape[0]
    print(f"\nRemoved {before_dupes - after_dupes} duplicate rows.")

    # Check for missing values
    print("\nMissing values by column:")
    print(df.isnull().sum())

    # Convert binary columns to int
    binary_cols = [
        "is_new_user",
        "clicked_recommendation",
        "watch_started",
        "signed_up",
        "retained_7d",
    ]
    for col in binary_cols:
        df[col] = df[col].fillna(0).astype(int)

    # Clean text columns
    text_cols = [
        "variant",
        "device_type",
        "traffic_source",
        "country",
        "age_group",
        "subscription_status",
    ]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().str.lower()

    # Validate variant values
    valid_variants = {"a", "b"}
    invalid_variant_rows = df[~df["variant"].isin(valid_variants)].shape[0]
    print(f"\nInvalid variant rows: {invalid_variant_rows}")

    # Basic numeric cleaning
    numeric_cols = ["pages_viewed", "minutes_watched", "session_duration_sec"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove impossible or broken values
    before_filter = df.shape[0]
    df = df[
        (df["pages_viewed"] >= 1) &
        (df["minutes_watched"] >= 0) &
        (df["session_duration_sec"] >= 0)
    ].copy()
    after_filter = df.shape[0]
    print(
        f"Removed {before_filter - after_filter} rows with invalid numeric values.")

    # Derived columns
    df["conversion"] = df["signed_up"]
    df["engaged_user"] = (
        (df["session_duration_sec"] > 180) | (df["pages_viewed"] >= 4)
    ).astype(int)
    df["high_watch_time"] = (df["minutes_watched"] > 30).astype(int)
    df["retention_proxy"] = df["retained_7d"]

    # Check A/B split
    print("\nVariant counts:")
    print(df["variant"].value_counts())

    print("\nVariant proportions:")
    print(df["variant"].value_counts(normalize=True))

    # Summary stats
    print("\nSummary stats:")
    print(
        df[
            [
                "pages_viewed",
                "minutes_watched",
                "session_duration_sec",
                "signed_up",
                "watch_started",
                "retained_7d",
            ]
        ].describe()
    )

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save clean dataset
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\nCleaned dataset saved to: {OUTPUT_PATH}")
    print("Clean shape:", df.shape)
    print("\nPreview:")
    print(df.head())


if __name__ == "__main__":
    main()
