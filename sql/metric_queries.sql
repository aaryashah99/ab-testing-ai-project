-- 1. Overall experiment performance by variant
SELECT
    variant,
    COUNT(*) AS sessions,
    AVG(signed_up) AS signup_rate,
    AVG(watch_started) AS watch_start_rate,
    AVG(clicked_recommendation) AS click_rate,
    AVG(session_duration_sec) AS avg_session_duration,
    AVG(minutes_watched) AS avg_minutes_watched,
    AVG(retained_7d) AS retention_rate
FROM read_csv_auto('data/processed/experiment_data_clean.csv')
GROUP BY variant
ORDER BY variant;


-- 2. Signup rate by device type and variant
SELECT
    device_type,
    variant,
    COUNT(*) AS sessions,
    AVG(signed_up) AS signup_rate
FROM read_csv_auto('data/processed/experiment_data_clean.csv')
GROUP BY device_type, variant
ORDER BY device_type, variant;


-- 3. Watch start rate by traffic source and variant
SELECT
    traffic_source,
    variant,
    COUNT(*) AS sessions,
    AVG(watch_started) AS watch_start_rate
FROM read_csv_auto('data/processed/experiment_data_clean.csv')
GROUP BY traffic_source, variant
ORDER BY traffic_source, variant;


-- 4. Retention rate by country and variant
SELECT
    country,
    variant,
    COUNT(*) AS sessions,
    AVG(retained_7d) AS retention_rate
FROM read_csv_auto('data/processed/experiment_data_clean.csv')
GROUP BY country, variant
ORDER BY country, variant;


-- 5. New vs returning user conversion by variant
SELECT
    is_new_user,
    variant,
    COUNT(*) AS sessions,
    AVG(signed_up) AS signup_rate,
    AVG(watch_started) AS watch_start_rate
FROM read_csv_auto('data/processed/experiment_data_clean.csv')
GROUP BY is_new_user, variant
ORDER BY is_new_user, variant;


-- 6. Top-performing segments by signup rate
SELECT
    device_type,
    traffic_source,
    is_new_user,
    variant,
    COUNT(*) AS sessions,
    AVG(signed_up) AS signup_rate
FROM read_csv_auto('data/processed/experiment_data_clean.csv')
GROUP BY device_type, traffic_source, is_new_user, variant
HAVING COUNT(*) >= 200
ORDER BY signup_rate DESC
LIMIT 15;


-- 7. Engagement metrics by age group and variant
SELECT
    age_group,
    variant,
    COUNT(*) AS sessions,
    AVG(session_duration_sec) AS avg_session_duration,
    AVG(minutes_watched) AS avg_minutes_watched,
    AVG(engaged_user) AS engaged_user_rate
FROM read_csv_auto('data/processed/experiment_data_clean.csv')
GROUP BY age_group, variant
ORDER BY age_group, variant;


-- 8. Variant uplift table by device type
WITH device_rates AS (
    SELECT
        device_type,
        variant,
        AVG(signed_up) AS signup_rate
    FROM read_csv_auto('data/processed/experiment_data_clean.csv')
    GROUP BY device_type, variant
)
SELECT
    a.device_type,
    a.signup_rate AS signup_rate_a,
    b.signup_rate AS signup_rate_b,
    (b.signup_rate - a.signup_rate) AS absolute_lift
FROM device_rates a
JOIN device_rates b
    ON a.device_type = b.device_type
WHERE a.variant = 'a'
  AND b.variant = 'b'
ORDER BY absolute_lift DESC;