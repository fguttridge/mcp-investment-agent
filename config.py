import os
import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()  # Loads GOOGLE_API_KEY from .env

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_model():
    return ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-8b",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)

def get_explanation_prompt():
    return ChatPromptTemplate.from_template(
        """
        You are an investment banking analyst reviewing the following financial summary:

        {summary}

        The initial investment recommendation is:

        {recommendation}

        Write a professional analysis that includes:
        - 📈 A **Bullish Case** (reasons to be optimistic based on the data)
        - 📉 A **Bearish Case** (risks or cautionary signs based on the data)
        - ✅ List 2-3 Strengths
        - ⚠️ List 2-3 Risks
        - 🎯 Conclude with an **Investment Score out of 10** and final recommendation tone (Buy / Hold / Sell).
        
        Keep the tone formal but actionable, as if preparing a client-facing memo. 
        
        format the result into an inline object as follows:
        {{
            bullish: substitute bullish case here,
            bearish: substitute bearish case here,
            recommendation: substitute recommendation here - lead with the recommendation and then include 2-3 risks and 2-3 strengths. Return HTML in a json body so that a webpage can use to display in good formatting, but avoid causing parsing errors
            investment_score: substitute the investment score out of 10 here
        }}
        """
    )