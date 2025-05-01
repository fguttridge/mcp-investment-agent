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

## 🧰 How to Diff with GitHub Repo

Run the following to compare this project to your GitHub version:

```bash
diff -rq ~/mcp-investment-agent /mnt/data/mcp-investment-agent-extracted/home/jp/mcp-investment-agent
```

Or for a detailed output:

```bash
diff -ru ~/mcp-investment-agent /mnt/data/mcp-investment-agent-extracted/home/jp/mcp-investment-agent | less
```

---

## 📜 License

MIT License