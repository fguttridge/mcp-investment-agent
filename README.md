# 💼 Investment Banking Assistant

An intelligent investment analysis assistant that performs the following:
- Extracts financial data from 10-K filings (via SEC EDGAR)
- Summarizes key metrics (e.g., Revenue, EPS, Free Cash Flow, ROE, P/E)
- Generates investment recommendations
- Provides sentiment analysis from recent news articles
- Responds to general-purpose financial queries with generative AI

## 📦 Features

- 🔍 **Financial Analysis Agent**  
  Parses latest 10-K filing, computes trends, and generates a buy/sell recommendation with justification.

- 🧠 **Generic AI Query Agent**  
  Handles general investment banking queries using OpenAI.

- 📰 **Sentiment Analysis Agent**  
  Fetches news from a public API and performs sentiment analysis to determine market tone (positive, neutral, or negative).

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/investment-agent.git
cd investment-agent
pip install -r requirements.txt
python app.py