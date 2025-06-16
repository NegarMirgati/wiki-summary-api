# app/summarizer.py

import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env
load_dotenv()

# Get API key
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # fallback default


def summarize_with_gpt(text: str, max_words: int = 300) -> str:
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    system_message = system_message = "You are a helpful assistant that"
    system_message += "summarizes Wikipedia articles in a clear, concise way"
    system_message += "Always be accurate. Make sure to not hallucinate."
    system_message += "Only make use of information that is given to you in the prompt."

    prompt = (
        "Summarize the following Wikipedia article content in a clear, concise way"
        f"in under {max_words} words:\n\n{text}"
    )


# app/summarizer.py

import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env
load_dotenv()

# Get API key
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # fallback default


def summarize_with_gpt(text: str, max_words: int = 300) -> str:
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    system_message = system_message = "You are a helpful assistant that "
    system_message += (
        "summarizes Wikipedia articles in a clear, coherent, and concise way."
    )
    system_message += "Always be accurate. Make sure to not hallucinate."
    system_message += "Only make use of information that is given to you in the prompt."

    prompt = (
        "Summarize the following Wikipedia article content in a clear, concise way"
        f"in under {max_words} words:\n\n{text}"
    )

    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
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
