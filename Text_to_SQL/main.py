from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from langchain_openai import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# Connect MySQL database

host = 'localhost'
port = '3306'
username = 'root'
password = 'atharv18M'
database_schema = 'text_to_sql'

mysql_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_schema}"

db = SQLDatabase.from_uri(mysql_uri,sample_rows_in_table_info=2)

db = SQLDatabase.from_uri(mysql_uri,sample_rows_in_table_info=1)

db.get_table_info()

# Create the LLM Prompt template

from langchain_core.prompts import ChatPromptTemplate

template = """Based on the table schema below, write a SQL query that would answer the user's question:
Remember : only provide me the sql query dont include anything else. Provide me sql query in a single line dont add line breaks
Table Schema: {schema}
Question: {question}
SQL Query:
"""

prompt = ChatPromptTemplate.from_template(template)

# get the schema of the database
def get_schema(db):
    schema = db.get_table_info()
    return schema

llm = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash',
    api_key = 'API_KEY'                 # make it private using .env
)

# Create the sql query chain using the LLM and the prompt template

sql_chain = (
    RunnablePassthrough.assign(schema=lambda _:get_schema(db))
    | prompt
    | llm.bind(stop={"\nSQLResult:"})
    | StrOutputParser()
)

# Test the SQL query chain with a simple question

resp = sql_chain.invoke({"question" : "what is sum of all total unit cost from orders "})
print("Query : ",resp)


  



