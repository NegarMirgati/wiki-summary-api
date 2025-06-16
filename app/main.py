# app/main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from markdown import markdown

from app.schemas import QueryRequest, SummaryResponse
from app.core import prepare_summary

import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Serve static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Serve the main HTML UI."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/summarize", response_model=SummaryResponse)
def summarize(request: QueryRequest):
    """
    JSON summary endpoint.
    Input:
      { "query": "Your question here" }

    Output:
      { "query": "...", "summary": "...", "source_url": "..." }
    """
    try:
        summary_text, url = prepare_summary(request.query, stream=False)
        return SummaryResponse(
            query=request.query, summary=summary_text, source_url=url
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/ui/summarize", response_class=HTMLResponse)
def summarize_ui(request: Request, query: str = Form(...)):
    """Handle form-based UI summarization (non-streaming)."""
    try:
        summary_text, url = prepare_summary(query, stream=False)

        # Convert Markdown to safe HTML
        summary_html = markdown(summary_text)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query,
                "summary": summary_html,
                "url": url,
            },
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query,
                "summary": f"<strong>Error:</strong> {str(e)}",
                "url": "#",
            },
        )


@app.post("/stream")
def stream_summary(request: QueryRequest):
    """Endpoint for streaming summary to client via SSE."""
    summary_generator, url = prepare_summary(request.query, stream=True)

    def generate():
        for chunk in summary_generator:
            delta = chunk.choices[0].delta
            if delta.content:
                yield f"data: {delta.content}\n\n"

        # Send URL at the end
        yield f"data: [SOURCE_URL]{url}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/health")
def health_check():
    """Basic health check endpoint."""
    return JSONResponse(content={"status": "ok"})
