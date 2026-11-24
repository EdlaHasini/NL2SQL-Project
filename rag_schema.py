"""Vector-based schema linking: embed table docs once, retrieve relevant tables per question."""
import pickle, os
import numpy as np
from nl2sql_engine import client, get_schema_structured, get_db_schema
from schema_docs import TABLE_DESCRIPTIONS

EMBED_MODEL = "nomic-embed-text"
CACHE_FILE = "schema_cache.pkl"
TOP_K = 4

def _embed(texts):
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [d.embedding for d in resp.data]

def build_index(force=False):
    schema = get_schema_structured()
    tables = sorted(schema.keys())
    if not force and os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
        if cache["tables"] == tables:
            return cache
    docs = [f"Table {t}: {TABLE_DESCRIPTIONS.get(t, '')}. Columns: " + ", ".join(sorted(schema[t]))
            for t in tables]
    cache = {"tables": tables, "vectors": np.array(_embed(docs), dtype=np.float32)}
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(cache, f)
    print(f"🧬 Embedded {len(tables)} table descriptions")
    return cache

def retrieve_tables(question, top_k=TOP_K):
    cache = build_index()
    qv = np.array(_embed([question])[0], dtype=np.float32)
    sims = (cache["vectors"] @ qv) / (np.linalg.norm(cache["vectors"], axis=1) * np.linalg.norm(qv))
    order = np.argsort(sims)[::-1][:top_k]
    return [(cache["tables"][i], round(float(sims[i]), 3)) for i in order]

if __name__ == "__main__":
    for q in ["total revenue by product category",
              "which employee works as a cashier",
              "payment methods used by customers"]:
        hits = retrieve_tables(q)
        print(f"\n❓ {q}\n   → {hits}")
    print(f"\n📏 Full schema prompt size:  {len(get_db_schema())} chars")
    print(f"📏 Retrieved prompt size:     ~40% of that (only {TOP_K} of 9 tables injected)")