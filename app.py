import streamlit as st
import pandas as pd
import nl2sql_engine
from nl2sql_engine import get_db_schema, generate_sql_with_retry, summarize_result
from visualizer import auto_visualize

st.set_page_config(page_title="AI SQL Analyst", layout="wide")

st.title("🤖 Natural Language to SQL Interface")
st.caption("Ask questions about your data. The AI generates safe, read-only SQL and visualizes it.")

if "schema" not in st.session_state:
    st.session_state.schema = get_db_schema()

with st.sidebar:
    st.subheader("🗄️ Database Schema")
    st.code(st.session_state.schema, language="sql")
    st.info("🔒 System is in strict READ-ONLY mode.")

user_query = st.text_input("Ask a question about your data:",
                           placeholder="e.g., 'What is the total revenue by product category?'")

if st.button("Generate & Run Query"):
    if not user_query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("🧠 Generating query, chart and insight..."):
            try:
                # 1) NL -> RAG retrieval -> safe SQL -> read-only execution (self-healing)
                sql_query, df = generate_sql_with_retry(user_query)

                # 2) Transparency: show SQL + which tables RAG selected
                st.code(sql_query, language="sql")
                st.caption(f"🔎 Schema retrieved from tables: {', '.join(nl2sql_engine.LAST_RETRIEVED)}")

                # 3) Dtype-aware auto-visualization
                st.subheader("📊 Results")
                visualization = auto_visualize(df)

                if isinstance(visualization, str):
                    if visualization.startswith("###"):
                        st.markdown(visualization)                          # single KPI value
                    else:
                        st.warning(visualization)                           # e.g. "No data returned"
                elif isinstance(visualization, pd.DataFrame):
                    st.dataframe(visualization, use_container_width=True)   # all-text results
                else:
                    st.plotly_chart(visualization, use_container_width=True)  # bar / line charts

                # 4) STEP 2.2 -> one-sentence AI insight BELOW the chart
                try:
                    insight = summarize_result(user_query, sql_query, df)
                    if insight:
                        st.info(f"💬 **Insight:** {insight}")
                except Exception:
                    pass  # bonus feature: never crash the app for it

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Tip: Try rephrasing your question.")