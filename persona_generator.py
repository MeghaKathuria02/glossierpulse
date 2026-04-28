import os

from dotenv import load_dotenv
from groq import Groq


# Load values from .env into environment variables.
load_dotenv()


def _get_groq_client() -> Groq:
    """
    Create a Groq client using GROQ_API_KEY from environment variables.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not set. Add your API key in your environment before running the app."
        )
    return Groq(api_key=api_key)


def build_persona_prompt(segment_name: str, segment_stats: dict) -> str:
    """
    Build a clear prompt for generating campaign personas in Glossier tone.
    """
    return f"""
You are a beauty marketing strategist for Glossier.

Brand voice rules:
- Honest and simple
- Skin-first and realistic
- Community-driven
- Never corporate, never salesy

Target segment: {segment_name}
Segment details:
- Customers: {segment_stats.get("customers")}
- Average age: {segment_stats.get("avg_age"):.1f}
- Average annual income: {segment_stats.get("avg_income"):.1f}
- Average spending score: {segment_stats.get("avg_spending"):.1f}
- Average purchase frequency: {segment_stats.get("avg_purchase_frequency"):.1f}

Create:
1) Persona name
2) Persona profile (2-3 lines)
3) Core skincare motivation
4) Main pain point
5) Best campaign message in Glossier voice (2-3 lines)
6) One social post caption idea
"""


def generate_persona_message(segment_name: str, segment_stats: dict) -> str:
    """
    Call Groq API to generate persona and campaign message text.
    """
    client = _get_groq_client()
    prompt = build_persona_prompt(segment_name=segment_name, segment_stats=segment_stats)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        messages=[
            {"role": "system", "content": "You write concise, friendly beauty marketing content."},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content.strip()
