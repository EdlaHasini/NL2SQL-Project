import streamlit as st
import pandas as pd
import sqlite3
from nl2sql_engine import get_db_schema, generate_sql_with_retry
from security import is_safe_query
from visualizer import auto_visualize

st.set_page_config(page_title="AI SQL Analyst", layout="wide")

st.title("🤖 Natural Language to SQL Interface")
st.caption("Ask questions about your data. The AI generates safe, read-only SQL and visualizes it.")

# Initialize session state
if "schema" not in st.session_state:
    st.session_state.schema = get_db_schema()

# Sidebar for schema inspection
with st.sidebar:
    st.subheader("🗄️ Database Schema")
    st.code(st.session_state.schema, language="sql")
    st.info("🔒 System is in strict READ-ONLY mode.")

# Main Interface
user_query = st.text_input("Ask a question about your data:", 
                           placeholder="e.g., 'What is the total revenue by product category?'")

if st.button("Generate & Run Query"):
    if not user_query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("🧠 AI is generating and executing the query..."):
            try:
                # 1. Call the new engine (returns both SQL and DataFrame)
                sql_query, df = generate_sql_with_retry(user_query)
                
                # 2. Show the generated SQL
                st.code(sql_query, language="sql")
                
                # 3. Visualize the results
                # 3. Visualize the results
                st.subheader("📊 Results")
                visualization = auto_visualize(df)

                if isinstance(visualization, str):
                    if visualization.startswith("###"):
                        st.markdown(visualization)
                    else:
                        st.warning(visualization)
                elif isinstance(visualization, pd.DataFrame):
                    st.dataframe(visualization, use_container_width=True)
                else:
                    st.plotly_chart(visualization, use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Tip: Try rephrasing your question.")