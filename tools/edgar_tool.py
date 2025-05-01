import os
import re
import requests
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI  # <-- Gemini
from langchain_core.tools import tool
from sec_edgar_downloader import Downloader
from config import get_explanation_prompt
from config import get_gemini_model

load_dotenv()

llm = get_gemini_model()

# === Utility: Fetch SEC Financial Statement Data API ===
def fetch_sec_financials(ticker):
    cik_lookup_url = "https://www.sec.gov/files/company_tickers.json"
    cik = None

    try:
        cik_data = requests.get(cik_lookup_url, headers={"User-Agent": os.getenv("EMAIL")}).json()
        for entry in cik_data.values():
            if entry['ticker'].upper() == ticker.upper():
                cik = str(entry['cik_str']).zfill(10)
                break
    except Exception as e:
        return None, f"❌ Failed to retrieve CIK for {ticker}: {e}"

    if not cik:
        return None, f"❌ CIK not found for ticker {ticker}"

    metrics = {
        "EPS Diluted": "EarningsPerShareDiluted",
        "Net Income": "NetIncomeLoss",
        "Revenue": "Revenues",
        "Total Assets": "Assets",
        "Total Liabilities": "Liabilities",
        "Shares Outstanding": "WeightedAverageNumberOfDilutedSharesOutstanding"
    }

    results = {}
    for label, concept in metrics.items():
        api_url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{concept}.json"
        try:
            response = requests.get(api_url, headers={"User-Agent": os.getenv("EMAIL")})
            data = response.json()
            units = data.get("units", {})

            for unit in ["USD", "USD/shares", "shares"]:
                if unit in units:
                    items = units[unit]
                    break
            else:
                continue

            years = []
            values = []
            for item in items:
                if 'end' in item and 'val' in item:
                    year = item['end'][:4]
                    if year.isdigit():
                        years.append(int(year))
                        values.append(item['val'])

            df = pd.DataFrame({"Year": years, label: values})
            df = df.drop_duplicates(subset=["Year"])
            df = df.sort_values(by="Year", ascending=False).head(5).reset_index(drop=True)
            results[label] = df
        except Exception as e:
            results[label] = pd.DataFrame(columns=["Year", label])

    merged_df = results["EPS Diluted"]
    for key, df in results.items():
        if key != "EPS Diluted":
            merged_df = pd.merge(merged_df, df, on="Year", how="outer")

    merged_df = merged_df.drop_duplicates(subset=["Year"])
    merged_df = merged_df.sort_values(by="Year", ascending=False).reset_index(drop=True)
    return merged_df, None

# === Generate Financial Analysis and Investment Recommendation ===
def generate_investment_recommendation(df):
    try:
        df["Revenue Growth Rate (%)"] = df["Revenue"].pct_change(-1) * 100
        df["EPS Growth Rate (%)"] = df["EPS Diluted"].pct_change(-1) * 100

        df["Shareholder Equity"] = df["Total Assets"] - df["Total Liabilities"]
        df["ROE (%)"] = (df["Net Income"] / df["Shareholder Equity"]) * 100
        df["Debt to Equity"] = df["Total Liabilities"] / df["Shareholder Equity"]

        # Estimate EBITDA (simple proxy)
        df["EBITDA"] = df["Net Income"] + (df["Revenue"] * 0.10)
        df["EBITDA Margin (%)"] = (df["EBITDA"] / df["Revenue"]) * 100

        df["Net Profit Margin (%)"] = (df["Net Income"] / df["Revenue"]) * 100

        # Estimate Free Cash Flow
        df["Free Cash Flow"] = df["Net Income"] - (df["Revenue"] * 0.10)

        # Estimate P/E Ratio
        df["P/E Ratio"] = (df["Shares Outstanding"] * df["EPS Diluted"]) / df["Net Income"]

        latest = df.iloc[0]
        score = 0
        if latest["Revenue Growth Rate (%)"] > 5: score += 1
        if latest["EPS Growth Rate (%)"] > 5: score += 1
        if latest["Net Profit Margin (%)"] > 10: score += 1
        if latest["EBITDA Margin (%)"] > 15: score += 1
        if latest["ROE (%)"] > 12: score += 1
        if latest["Debt to Equity"] < 1: score += 1
        if latest["Free Cash Flow"] > 0: score += 1
        if latest["P/E Ratio"] and latest["P/E Ratio"] < 25: score += 1

        if score >= 6:
            recommendation = "✅ **Buy Recommendation**: Strong financial performance."
        elif score >= 4:
            recommendation = "🤔 **Hold Recommendation**: Moderate performance with some risks."
        else:
            recommendation = "❌ **Sell Recommendation**: Weak fundamentals."

        explanation_prompt = get_explanation_prompt()
        chain = explanation_prompt | llm | RunnableLambda(lambda x: x.content)

        explanation = chain.invoke({
            "summary": df.to_string(index=False),
            "recommendation": recommendation
        })

        parsed_response = parse_llm_response(explanation)

        # Add the score to the response before returning
        return {
            **parsed_response,
            "investment_score": score
        }

    except Exception as e:
        print(f"⚠️ Error generating recommendation: {e}")
        return {
            "bullish": "Error generating analysis",
            "bearish": "Error generating analysis",
            "recommendation": "Error generating analysis",
            "investment_score": "Error generating analysis"
        }

# === Main Function ===
def fetch_edgar_data(ticker: str, download_dir="sec-edgar-filings"):
    dl = Downloader(download_dir, email_address=os.getenv("EMAIL"))
    try:
        dl.get("10-K", ticker.upper())
        print(f"✅ Downloaded 10-K filings for {ticker}")
    except Exception as e:
        return {"error": f"❌ Failed to download data: {e}"}

    df, err = fetch_sec_financials(ticker)
    if err:
        return {"error": err}

    analysis = generate_investment_recommendation(df)

    output_file = f"{ticker.upper()}_Investment_Summary.xlsx"
    df.to_excel(output_file, index=False)

    return {
        "ticker": ticker.upper(),
        "financial_summary_table": df.to_dict(orient="records"),
        "analysis": analysis,
        "file_saved": output_file
    }

# === LangChain Tool ===
@tool
def edgar_financials_tool(ticker: str) -> dict:
    """Given a stock ticker, pulls financial metrics from SEC API and generates a professional investment summary."""
    return fetch_edgar_data(ticker)

def parse_llm_response(response: str):
    """
    Parse the LLM response to extract the bullish case, bearish case, and recommendation.
    Returns a dictionary with these sections.
    """
    # Strip any extra whitespace and remove the markdown code block syntax
    response = response.strip()

    # Remove the markdown block ` ```json ` and ending ` ``` ` if present
    response = re.sub(r'```json\n|\n```', '', response)

    # Log the raw cleaned response for debugging
    print("Cleaned Response for Parsing:\n", repr(response))  # Debugging output

    if not response:
        print("Error: Received an empty response.")  # Debugging output for empty responses
        return {"bullish": "No response received", "bearish": "No response received", "recommendation": "No response received", "investment_score": "No response received"}

    try:
        # Clean up escape sequences
        response = re.sub(r'\\n', ' ', response)  # Replace \\n with a space
        response = re.sub(r'\\(.)', r'\1', response)  # Remove other escaped characters

        # Try to parse the cleaned response string as a JSON object
        response_data = json.loads(response)
        print("Parsed Response Data:\n", response_data)  # Print the parsed data for debugging
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")  # Debugging output for any parsing issues
        return {"bullish": "Error parsing response", "bearish": "Error parsing response", "recommendation": "Error parsing response", "investment_score": "Error parsing response"}

    # Ensure that response_data is a dictionary
    if isinstance(response_data, dict):
        # Extract Bullish Case, Bearish Case, Recommendation, and Investment Score directly from the response
        bullish = response_data.get("bullish", "Not found")
        bearish = response_data.get("bearish", "Not found")
        recommendation = response_data.get("recommendation", "Not found")
        investment_score = response_data.get("investment_score", "Not found")

        # Return the parsed content as a dictionary
        return {
            "bullish": bullish,
            "bearish": bearish,
            "recommendation": recommendation,
            "investment_score": investment_score
        }
    else:
        print("Error: Parsed response is not a dictionary.")  # Debugging output
        return {"bullish": "Error: Invalid response format", "bearish": "Error: Invalid response format", "recommendation": "Error: Invalid response format", "investment_score": "Error: Invalid response format"}