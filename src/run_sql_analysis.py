import duckdb
import os

SQL_FILE = "sql/metric_queries.sql"
OUTPUT_DIR = "outputs/reports"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_text = f.read()

queries = [q.strip() for q in sql_text.split(";") if q.strip()]

con = duckdb.connect()

for i, query in enumerate(queries, start=1):
    print(f"\n{'=' * 80}")
    print(f"QUERY {i}")
    print(f"{'=' * 80}")
    result = con.execute(query).fetchdf()
    print(result)

    output_path = os.path.join(OUTPUT_DIR, f"sql_query_{i}.csv")
    result.to_csv(output_path, index=False)

print("\nAll SQL query outputs saved to outputs/reports/")