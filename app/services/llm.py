from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None


def ask_llm(prompt: str, tool_result: dict | None = None) -> str:

    if tool_result:
        prompt = f"""
User question:
{prompt}

Deterministic marine safety tool result:
{tool_result}

Explain the tool result clearly to the user.
Do not invent coordinates, distances, boundaries, weather conditions,
or other facts that are not present in the tool result.
The deterministic tool result must be treated as authoritative.
"""

    if client is None:
        return f"[MOCK LLM] Query: {prompt}"

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception:
        return f"[MOCK LLM] API unavailable. Query: {prompt}"
