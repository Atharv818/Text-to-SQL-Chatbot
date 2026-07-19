# Text-to-SQL Chatbot

An AI-powered chatbot that converts plain English questions into optimized SQL queries, using Google's Gemini LLM and LangChain — built with an agentic workflow that reads the live database schema and generates accurate, context-aware SQL.

## How It Works
1. Connects to a MySQL database and reads its schema
2. Takes a natural language question as input
3. Passes the schema + question to Gemini via a LangChain prompt chain
4. Returns a ready-to-run SQL query

## Tech Stack
- **LangChain** — orchestration and prompt chaining
- **Google Gemini (gemini-2.5-flash)** — LLM for SQL generation
- **MySQL + PyMySQL** — database connection
- **python-dotenv** — environment variable management

## Setup

1. Clone the repo and install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. Copy \`.env.example\` to \`.env\` and fill in your actual database credentials and Gemini API key:
   \`\`\`bash
   cp .env.example .env
   \`\`\`

3. Run:
   \`\`\`bash
   python src/main.py
   \`\`\`

## Sample Data
The \`data/\` folder contains sample CSVs (Products, Regions, Customers, Orders, Budgets) used to populate the test database schema this project was built against.

## Example
**Question:** "What is the sum of all total unit cost from orders?"
**Generated SQL:** \`SELECT SUM(total_unit_cost) FROM orders;\`
