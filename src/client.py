"""Creates the Groq API client from the GROQ_API_KEY environment variable."""

import os

from dotenv import load_dotenv
from groq import Groq


def get_client():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("No GROQ_API_KEY found. Put it in your .env file.")
    return Groq(api_key=api_key)
