from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.schemas import QueryRequest, SummaryResponse
from app.scraper import get_wikipedia_summary
from app.summarizer import summarize_with_gpt

import logging

app = FastAPI()

# Serve templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ui/summarize", response_class=HTMLResponse)
def summarize_ui(request: Request, query: str = Form(...)):
    try:
        text, url = get_wikipedia_summary(query)
        summary = summarize_with_gpt(text)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query,
                "summary": summary,
                "url": url,
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query,
                "summary": f"Error: {str(e)}",
                "url": "#",
            },
        )
