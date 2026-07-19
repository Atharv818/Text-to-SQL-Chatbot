import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env
load_dotenv()

# --- Database connection ---
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
database_schema = os.getenv("DB_NAME")

mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"
db = SQLDatabase.from_uri(mysql_uri, sample_rows_in_table_info=2)

# --- Prompt template ---
template = """Based on the table schema below, write a SQL query that would answer the user's question:
Remember: only provide the SQL query, don't include anything else. Provide the SQL query in a single line, don't add line breaks.

Table Schema: {schema}
Question: {question}
SQL Query:
"""
prompt = ChatPromptTemplate.from_template(template)


def get_schema(_):
    """Fetch the current database schema as context for the LLM."""
    return db.get_table_info()


# --- LLM setup ---
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
)

# --- Build the SQL generation chain ---
sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm.bind(stop=["\nSQLResult:"])
    | StrOutputParser()
)

if __name__ == "__main__":
    question = "What is the sum of all total unit cost from orders?"
    response = sql_chain.invoke({"question": question})
    print("Query:", response)


