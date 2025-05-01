import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from prompts.investment_prompt import get_explanation_prompt

load_dotenv()  # Loads from .env file


def get_gemini_model():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-8b",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0,
    )


def get_openai_model():
    return ChatOpenAI(
        model="gpt-4",  # Adjust if you prefer gpt-3.5-turbo
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
    )