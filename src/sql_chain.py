import os
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

from build_db import DB_PATH, build_database

TEMPLATE = """Based on the table schema below, write a SQL query that would answer the user's question:
Remember: only provide the SQL query, don't include anything else. Provide the SQL query in a single line, don't add line breaks.

Table Schema: {schema}
Question: {question}
SQL Query:
"""


def get_db():
    """Ensures the SQLite DB exists, then returns a connected SQLDatabase."""
    if not os.path.exists(DB_PATH):
        build_database()
    return SQLDatabase.from_uri(f"sqlite:///{DB_PATH}", sample_rows_in_table_info=2)


def get_schema(db):
    return db.get_table_info()


def build_chain(api_key: str):
    db = get_db()
    prompt = ChatPromptTemplate.from_template(TEMPLATE)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

    chain = (
        RunnablePassthrough.assign(schema=lambda _: get_schema(db))
        | prompt
        | llm.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
    )
    return chain, db


def run_query(db, sql_query: str):
    """Executes the generated SQL against the database and returns raw results."""
    return db.run(sql_query)
