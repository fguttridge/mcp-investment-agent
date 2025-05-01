# router_prompt.py
from langchain_core.prompts import PromptTemplate

router_prompt = PromptTemplate.from_template("""
You are an AI assistant with access to tools.

Classify the user input. Return one of:
- action: "calculate" if it's a math question (e.g. "sqrt(25)+5")
- action: "respond" if it's a general question
- action: "edgar" if it's a question about company financials, or a particular buy/sell stock question
    - in the case the action is edgar please rewrite the user input to include only the ticker for the company

Respond in JSON like this:
{{"action": "calculate"}}

User input: {input}
""")