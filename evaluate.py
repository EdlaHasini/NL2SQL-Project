"""Evaluation harness: measures NL2SQL execution accuracy on a fixed benchmark."""
import time
import pandas as pd
from nl2sql_engine import generate_sql_with_retry

TEST_CASES = [
    {"q": "List all customers with their name and emails", "rows": 2, "cols": 2},
    {"q": "Show total quantity sold per product category", "rows": 3, "sql_contains": ["JOIN", "GROUP BY"]},
    {"q": "What is the average price of all products?", "rows": 1, "cols": 1},
    {"q": "Which customers signed up after March 1, 2023?", "rows": 1},
    {"q": "How many orders were placed in total?", "rows": 1, "cols": 1},
    {"q": "Show the names of products in the Electronics category", "rows": 1},
    {"q": "List product names and prices sorted from highest to lowest", "sql_contains": ["ORDER BY"]},
    {"q": "What is the total revenue (quantity times price) per category?", "rows": 3, "sql_contains": ["JOIN", "GROUP BY"]},
]

def run_evaluation():
    results = []
    print(f"\n🧪 Running benchmark on {len(TEST_CASES)} questions...\n")
    for i, tc in enumerate(TEST_CASES, 1):
        t0 = time.time()
        try:
            sql, df = generate_sql_with_retry(tc["q"])
            checks = []
            if "rows" in tc: checks.append(df.shape[0] == tc["rows"])
            if "cols" in tc: checks.append(df.shape[1] == tc["cols"])
            if "sql_contains" in tc:
                checks.append(all(k.lower() in sql.lower() for k in tc["sql_contains"]))
            passed, err = all(checks), ""
        except Exception as e:
            sql, passed, err = "", False, str(e)[:80]
        results.append({"id": i, "question": tc["q"], "sql": sql,
                        "passed": passed, "error": err,
                        "seconds": round(time.time() - t0, 1)})
        print(f"{'✅' if passed else '❌'} Q{i}: {tc['q'][:55]:<55} {err}")

    df_res = pd.DataFrame(results)
    df_res.to_csv("eval_results.csv", index=False)
    acc = df_res["passed"].mean() * 100
    print("\n" + "=" * 60)
    print(f"📊 EXECUTION ACCURACY: {df_res['passed'].sum()}/{len(df_res)}  ({acc:.0f}%)")
    print(f"⏱️  Avg latency: {df_res['seconds'].mean():.1f}s per question")
    print("=" * 60)

if __name__ == "__main__":
    run_evaluation()