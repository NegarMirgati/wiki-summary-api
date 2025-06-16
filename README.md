# Wiki Summary API

This project is a take-home assignment for FairlaneAI. It’s a FastAPI-based web service that takes a natural language query (e.g., *"Tell me the history of Agentic AI"*) and returns a clean, concise summary of the relevant Wikipedia article. It uses OpenAI's GPT models for both topic extraction and summarization.



## Features

- Accepts natural-language user queries via a POST API or a simple browser UI
- Uses an LLM to extract the actual Wikipedia topic from the query
- Scrapes and parses the correct Wikipedia page
- Summarizes the content using a GPT model of your choice
- Returns the summary and source URL in JSON or in a browser view


## Tech Stack

- FastAPI for the backend API
- OpenAI GPT (via `openai` Python SDK) for summarization and topic extraction
- Wikipedia API (`wikipedia` Python package) for content retrieval
- Jinja2 + HTML for a minimal optional frontend
- `.env`-based configuration for secrets and model selection



## Setup Instructions

### 1. Clone the repo and set up your environment

```bash
git clone https://github.com/your-username/wiki-summary-api.git
cd wiki-summary-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

### 2. Set up environment variables
```bash
cp .env.example .env
````

Then open .env and set your OpenAI API key and model.


### 3. Run the application
```bash
uvicorn app.main:app --reload
````
Then open:

- http://127.0.0.1:8000/docs for the API `Swagger UI`  
- http://127.0.0.1:8000/ for the simple `browser UI`


## Usage

You can test the summarization service in **two ways**:

### 1. API (via Postman, cURL, etc.)

Make a `POST` request to `/summarize` with a JSON payload:

```bash
curl -X POST http://127.0.0.1:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"query":"Tell me the history of Agentic AI"}'
```


### 2. Live Browser UI
For a more interactive experience, use the built-in web interface:

**Step 1: Start the app**

   ```bash
   uvicorn app.main:app --reload
   ```
**Step 2: Open your browser and navigate to**
   
   ```bash
   http://127.0.0.1:8000/
   ```