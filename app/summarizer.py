# app/summarizer.py

import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env
load_dotenv()

# Get API key
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # fallback default

client = openai.OpenAI()  # Automatically picks up OPENAI_API_KEY from env


def summarize_with_gpt(text: str, max_words: int = 300, stream: bool = False):
    """
    Use OpenAI's GPT model to summarize a given text.

    If stream=True, return a generator yielding delta chunks.
    Otherwise, return the full summary string.
    """
    system_message = (
        "You are a helpful assistant that summarizes Wikipedia articles in a clear, "
        "coherent, and concise way. Always be accurate. Do not hallucinate. "
        "Only use information provided in the prompt."
    )

    prompt = f"Summarize the following Wikipedia article content in under {max_words} words:\n\n{text}"

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt},
    ]

    if stream:
        # Return the raw generator for the caller to handle chunking
        return client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            messages=messages,
            temperature=0.7,
            stream=True,
        )
    else:
        # Return a single response string
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4"), messages=messages, temperature=0.7
        )
        return response.choices[0].message.content.strip()


def extract_topic_with_llm(query: str) -> str:
    """
    Uses the LLM to extract the most relevant Wikipedia topic from the full user query.
    """
    system_message = (
        "You are a helpful assistant that extracts concise Wikipedia search terms "
        "from longer user questions. Only return the clean topic name, nothing else."
    )

    prompt = f"What is the best Wikipedia search term for this user query:\n{query}"

    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
