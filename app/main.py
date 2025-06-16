from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, JSONResponse

from app.schemas import QueryRequest

from app.scraper import get_wikipedia_summary
from app.summarizer import summarize_with_gpt

from markdown import markdown

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

        # Convert markdown-style formatting to HTML
        summary_html = markdown(summary)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "query": query,
                "summary": summary_html,  # pass HTML version
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
    content, url = get_wikipedia_summary(request.query)
    gpt_stream = summarize_with_gpt(content, stream=True)

    def generate():
        for chunk in gpt_stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield f"data: {delta.content}\n\n"

        yield f"data: [SOURCE_URL]{url}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})
