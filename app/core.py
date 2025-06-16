# app/core.py

from app.scraper import get_wikipedia_summary
from app.summarizer import summarize_with_gpt


def prepare_summary(query: str, stream: bool = False):
    text, url = get_wikipedia_summary(query)
    if stream:
        # return the streaming generator and the URL
        return summarize_with_gpt(text, stream=True), url
    else:
        # return the full summary text and the URL
        return summarize_with_gpt(text, stream=False), url
