import os
import numpy as np
import pandas as pd

# Reproducibility
np.random.seed(42)

# Number of sessions
N = 50000

# Create IDs
user_ids = np.random.randint(10000, 99999, size=N)
session_ids = np.arange(1, N + 1)

# Random experiment assignment
variant = np.random.choice(["A", "B"], size=N, p=[0.5, 0.5])

# User/device/source features
device_type = np.random.choice(
    ["mobile", "desktop", "tablet"],
    size=N,
    p=[0.6, 0.3, 0.1]
)

traffic_source = np.random.choice(
    ["organic", "paid_social", "paid_search", "email", "direct"],
    size=N,
    p=[0.3, 0.2, 0.2, 0.1, 0.2]
)

country = np.random.choice(
    ["US", "India", "UK", "Canada", "Germany"],
    size=N,
    p=[0.35, 0.25, 0.15, 0.15, 0.10]
)

is_new_user = np.random.choice([0, 1], size=N, p=[0.45, 0.55])

age_group = np.random.choice(
    ["18-24", "25-34", "35-44", "45-54", "55+"],
    size=N,
    p=[0.2, 0.35, 0.2, 0.15, 0.1]
)

# Pages viewed
pages_viewed = np.random.poisson(lam=4, size=N) + 1

# Base click probability
click_prob = np.where(variant == "A", 0.22, 0.25)
click_prob += np.where(device_type == "desktop", 0.02, 0)
click_prob += np.where(traffic_source == "email", 0.03, 0)
click_prob += np.where(is_new_user == 1, -0.01, 0)
click_prob = np.clip(click_prob, 0.01, 0.95)

clicked_recommendation = np.random.binomial(1, click_prob)

# Watch start probability
watch_prob = np.where(variant == "A", 0.12, 0.14)
watch_prob += 0.08 * clicked_recommendation
watch_prob += np.where(traffic_source == "direct", 0.02, 0)
watch_prob += np.where(device_type == "mobile", -0.01, 0)
watch_prob = np.clip(watch_prob, 0.01, 0.95)

watch_started = np.random.binomial(1, watch_prob)

# Minutes watched
minutes_watched = np.where(
    watch_started == 1,
    np.random.gamma(shape=2.5, scale=12, size=N),
    np.random.gamma(shape=1.0, scale=2, size=N)
)
minutes_watched = np.round(minutes_watched, 2)

# Signup probability
signup_prob = np.where(variant == "A", 0.045, 0.052)
signup_prob += 0.03 * clicked_recommendation
signup_prob += 0.04 * watch_started
signup_prob += np.where(traffic_source == "email", 0.015, 0)
signup_prob += np.where(is_new_user == 1, 0.01, -0.005)
signup_prob = np.clip(signup_prob, 0.001, 0.95)

signed_up = np.random.binomial(1, signup_prob)

# 7-day retention proxy
retention_prob = 0.08 + 0.18 * signed_up + 0.12 * watch_started
retention_prob += np.where(device_type == "desktop", 0.02, 0)
retention_prob = np.clip(retention_prob, 0.01, 0.95)

retained_7d = np.random.binomial(1, retention_prob)

# Session duration
session_duration_sec = (
    pages_viewed * np.random.randint(20, 60, size=N)
    + clicked_recommendation * np.random.randint(15, 45, size=N)
    + watch_started * np.random.randint(60, 600, size=N)
)
session_duration_sec = session_duration_sec.astype(int)

# Subscription status after session
subscription_status = np.where(signed_up == 1, "subscribed", "not_subscribed")

# Build dataframe
df = pd.DataFrame({
    "user_id": user_ids,
    "session_id": session_ids,
    "variant": variant,
    "device_type": device_type,
    "traffic_source": traffic_source,
    "country": country,
    "is_new_user": is_new_user,
    "age_group": age_group,
    "pages_viewed": pages_viewed,
    "clicked_recommendation": clicked_recommendation,
    "watch_started": watch_started,
    "minutes_watched": minutes_watched,
    "signed_up": signed_up,
    "retained_7d": retained_7d,
    "session_duration_sec": session_duration_sec,
    "subscription_status": subscription_status
})

# Create output folder if it does not exist
output_path = "data/raw"
os.makedirs(output_path, exist_ok=True)

# Save CSV
file_path = os.path.join(output_path, "experiment_data.csv")
df.to_csv(file_path, index=False)

print("Dataset generated successfully.")
print(f"Saved to: {file_path}")
print(df.head())
print("\nShape:", df.shape)
print("\nVariant distribution:")
print(df["variant"].value_counts(normalize=True))