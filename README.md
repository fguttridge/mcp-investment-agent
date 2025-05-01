# 💼 MCP Investment Agent

An agent-powered investment analysis assistant that uses multiple LLMs (OpenAI + Gemini) to analyze 10-K filings and other financial inputs. Supports agentic model selection, dynamic prompt routing, and structured output.

---

## 🚀 Features

- 🧠 **Agentic model selection** using prompt-based logic.
- 🧾 **Structured financial prompts** with Bullish/Bearish/Recommendation breakdowns.
- 🔄 **Model override** via UI dropdown (OpenAI, Gemini, Auto).
- 📁 **EDGAR integration** to download 10-K filings for companies.
- 📤 **Dynamic JSON responses** for future-proof frontend rendering.

---

## 🗂️ Project Layout

```
mcp-investment-agent/
├── app.py                      # Flask entrypoint
├── config.py                   # Loads and configures LLM models
├── requirements.txt
├── README.md
├── templates/
│   └── index.html              # UI template
├── static/
│   ├── script.js               # Handles submission + overrides
│   └── style.css
├── router/
│   ├── router_runner.py        # Main routing logic
│   ├── router_chain.py         # Model dispatching pipeline
│   └── model_router.py         # Chooses LLM (auto/manual)
├── prompts/
│   ├── investment_prompt.py    # Prompt for financial analysis
│   └── router_model_selector.py # Prompt to help select LLM
├── tools/
│   └── edgar_tool.py etc.      # Additional analysis tools
└── test_router_chain.py
```

---

## 🧪 Model Override Options

From the dropdown menu in the UI:
- `Auto` → Uses agentic decision logic
- `OpenAI` → Forces GPT-4 response
- `Gemini` → Forces Gemini 1.5 Flash response

---


## 🚀 Setup Instructions
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/investment-agent.git
cd investment-agent
pip install -r requirements.txt
python app.py

## 📜 License

MIT License