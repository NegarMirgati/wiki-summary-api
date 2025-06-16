# Wiki Summary API

This is the take-home assignment project for FairlaneAI. It’s a FastAPI-based service that takes a natural language query (e.g., "Give me the history of Agentic AI") and returns a concise summary of the relevant Wikipedia article using an LLM.

---

## Features

- Accepts user queries via a `/summarize` POST endpoint
- Scrapes relevant Wikipedia content based on the query
- Summarizes the content using a language model (LLM)
- Returns a clean JSON response with the query, summary, and source URL

---

## Tech Stack

- FastAPI – for API development
- BeautifulSoup / Requests – for web scraping
- LLM (#TODO) – for summarization

---

## Installation

```bash
git clone https://github.com/NegarMirgati/wiki-summary-api.git
cd wiki-summary-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt