import os
import streamlit as st
from dotenv import load_dotenv
from sql_chain import build_chain, run_query

load_dotenv()

st.set_page_config(page_title="Text-to-SQL Chatbot", page_icon="💬", layout="centered")

st.title("💬 Text-to-SQL Chatbot")
st.caption("Ask a question in plain English — get a live SQL query and its result, powered by Gemini + LangChain.")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY is not set. Add it to your .env file (locally) or environment variables (on Render).")
    st.stop()

if "chain" not in st.session_state:
    with st.spinner("Setting up database and AI chain..."):
        st.session_state.chain, st.session_state.db = build_chain(api_key)

st.markdown("**Try asking things like:**")
st.markdown("- What is the total budget across all regions?\n- List all products with their prices\n- How many orders are there in total?")

question = st.text_input("Your question:", placeholder="e.g. What is the sum of all total unit cost from orders?")

if st.button("Generate & Run Query", type="primary") and question:
    with st.spinner("Generating SQL query..."):
        sql_query = st.session_state.chain.invoke({"question": question})
        sql_query_clean = sql_query.strip().strip("`").replace("sql\n", "").strip()

    st.subheader("Generated SQL")
    st.code(sql_query_clean, language="sql")

    with st.spinner("Running query..."):
        try:
            result = run_query(st.session_state.db, sql_query_clean)
            st.subheader("Result")
            st.write(result)
        except Exception as e:
            st.error(f"Query execution failed: {e}")

st.divider()
st.caption("Built by Atharv Mandhare · [GitHub](https://github.com/Atharv818) · Data: sample sales/products/regions dataset")
