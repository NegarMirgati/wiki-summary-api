# app/scraper.py

import wikipedia
from typing import Tuple


from app.summarizer import extract_topic_with_llm


def get_wikipedia_summary(query: str) -> Tuple[str, str]:
    try:
        refined_topic = extract_topic_with_llm(query)
        search_results = wikipedia.search(refined_topic)

        if not search_results:
            raise ValueError(f"No Wikipedia results for: {refined_topic}")

        top_result = search_results[0]
        page = wikipedia.page(top_result, auto_suggest=False)
        return page.content, page.url

    except wikipedia.DisambiguationError as e:
        fallback = e.options[0]
        page = wikipedia.page(fallback)
        return page.content, page.url

    except wikipedia.PageError:
        raise ValueError(f"No Wikipedia page found for query: {query}")
