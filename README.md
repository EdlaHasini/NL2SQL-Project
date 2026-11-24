# 🤖 AI SQL Analyst — Natural Language → SQL Interface

Ask questions in plain English. The app generates **safe, read-only SQL**, runs it on a local
SQLite database, and **auto-visualizes** the result — powered by a fully local LLM (Ollama).

## ✨ Features
- Natural-language to SQL via local `qwen2.5-coder:7b` (no cloud, full privacy)
- 3-layer safety: prompt rules → sqlparse keyword gate → read-only DB connection
- Deterministic identifier grounding (auto-fixes `customer` → `customers`)
- Agentic self-correction: failed queries are retried with the error fed back
- Dtype-aware auto-visualization (KPI / line / bar / table) with Plotly

## 🚀 Quickstart
1. Install [Ollama](https://ollama.com) and run: `ollama pull qwen2.5-coder:7b`
2. `pip install -r requirements.txt`
3. `python setup_db.py`   (creates the sample e-commerce database)
4. `streamlit run app.py`

## 🏗️ Architecture
Question → Schema-aware prompt → LLM → Identifier grounding → Security gate
→ Read-only execution → Dtype-aware visualization (→ self-healing retry on error)

## 📄 Report
See `REPORT.md` for the full project report.