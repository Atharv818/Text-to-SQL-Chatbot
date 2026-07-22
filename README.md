# Text-to-SQL Chatbot

An AI-powered chatbot that converts plain English questions into optimized SQL queries and runs them live — built with Gemini, LangChain, and a Streamlit interface.

🔗 **Live Demo:** _(add your Render link here once deployed)_

## How It Works
1. Sample business data (products, regions, orders, customers, budgets) is loaded into a local SQLite database
2. You ask a question in plain English via the Streamlit UI
3. LangChain + Gemini read the database schema and generate an accurate SQL query
4. The query runs automatically and the result is displayed — no SQL knowledge required

## Tech Stack
- **Streamlit** — interactive web UI
- **LangChain** — prompt orchestration
- **Google Gemini (gemini-2.5-flash)** — SQL generation
- **SQLite + Pandas** — lightweight, zero-setup database built from CSVs

## Setup

1. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. Copy \`.env.example\` to \`.env\` and add your Gemini API key:
   \`\`\`bash
   cp .env.example .env
   \`\`\`

3. Run:
   \`\`\`bash
   streamlit run src/app.py
   \`\`\`

The SQLite database is built automatically on first run from the CSVs in \`data/\`.

## Example
**Question:** "What is the sum of all total unit cost from orders?"
**Generated SQL:** \`SELECT SUM(total_unit_cost) FROM orders;\`
