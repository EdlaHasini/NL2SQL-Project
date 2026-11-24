import sqlite3, re, difflib
import pandas as pd
import sqlparse
from sqlparse.tokens import Name
from openai import OpenAI
from security import is_safe_query

LAST_RETRIEVED = []   # for UI display

def get_relevant_schema(question):
    """RAG: inject only the tables relevant to this question."""
    global LAST_RETRIEVED
    from rag_schema import retrieve_tables          # lazy import avoids circular dependency
    hits = retrieve_tables(question)
    LAST_RETRIEVED = [t for t, _ in hits]
    schema = get_schema_structured()
    return "\n".join(f"Table: {t}\nColumns: {', '.join(sorted(schema[t]))}" for t in LAST_RETRIEVED)

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL_NAME = "qwen2.5-coder:7b"   # or "sqlcoder"
DB_PATH = "ecommerce.db"

def _conn_ro():
    return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)

# ---------- Schema helpers ----------
def get_schema_structured():
    conn = _conn_ro(); cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    schema = {}
    for t in tables:
        cur.execute(f"PRAGMA table_info({t})")
        schema[t] = {r[1] for r in cur.fetchall()}
    conn.close()
    return schema

def get_db_schema():
    s = get_schema_structured()
    return "\n".join(f"Table: {t}\nColumns: {', '.join(sorted(c))}" for t, c in s.items())

# ---------- Layer 1: deterministic identifier grounding ----------
SQL_KEYWORDS = {"select","from","where","group","order","by","join","on","as",
                "sum","avg","count","max","min","and","or","not","limit","having"}

def ground_identifiers(sql, schema):
    known = {t.lower() for t in schema}
    for cols in schema.values():
        known |= {c.lower() for c in cols}
    parsed = sqlparse.parse(sql)[0]
    fixes = {}
    for tok in parsed.flatten():
        if tok.ttype in (Name,):
            val = tok.value.lower()
            if len(val) < 3 or val in known or val in SQL_KEYWORDS:
                continue
            match = difflib.get_close_matches(val, list(known), n=1, cutoff=0.85)
            if match:
                fixes[val] = match[0]
    out = sql
    for wrong, right in fixes.items():
        out = re.sub(rf"\b{re.escape(wrong)}\b", right, out, flags=re.IGNORECASE)
    return out, fixes

# ---------- Layer 2: agentic self-correction ----------
def generate_sql_with_retry(nl_query, max_retries=3):
    schema_str = get_relevant_schema(nl_query)
    schema_struct = get_schema_structured()
    messages = [{"role": "user", "content": f"""
You are an expert data analyst. Translate the question into a valid SQLite query.
Rules:
1. Use ONLY the exact table and column names from the schema (respect pluralization).
2. Return ONLY raw SQL — no markdown, no comments, no sentences.
3. Use JOINs with table aliases when relating tables.

Schema:
{schema_str}

Question: {nl_query}
SQL:"""}]

    last_err = None
    for _ in range(max_retries):
        resp = client.chat.completions.create(model=MODEL_NAME, messages=messages, temperature=0.1)
        raw = resp.choices[0].message.content.strip()
        sql = raw.replace("```sql", "").replace("```", "").strip()

        sql, fixed = ground_identifiers(sql, schema_struct)   # Layer 1
        if fixed:
            print("🔧 Auto-corrected identifiers:", fixed)

        if not is_safe_query(sql):                            # security gate
            raise PermissionError("Generated query is not read-only.")

        try:
            conn = _conn_ro()
            df = pd.read_sql_query(sql, conn)
            conn.close()
            return sql, df                                    # ✅ success
        except Exception as e:
            last_err = str(e)                                 # Layer 2: feed error back
            messages += [
                {"role": "assistant", "content": sql},
                {"role": "user", "content": f"The query failed: {last_err}. "
                                            f"Use EXACT names from the schema. Return only corrected SQL."}
            ]
    raise RuntimeError(f"Failed after {max_retries} tries. Last error: {last_err}")


def summarize_result(question, sql, df):
    """LLM writes a one-sentence business insight from the result preview."""
    if df.empty:
        return None
    preview = df.head(5).to_string(index=False)
    prompt = (f"You are a data analyst. Answer in ONE plain sentence using only this data.\n"
              f"Question: {question}\nData preview:\n{preview}\nSentence:")
    resp = client.chat.completions.create(model=MODEL_NAME,
                                          messages=[{"role": "user", "content": prompt}],
                                          temperature=0.2)
    return resp.choices[0].message.content.strip()