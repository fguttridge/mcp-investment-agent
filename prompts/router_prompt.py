from langchain_core.prompts import ChatPromptTemplate

router_prompt = ChatPromptTemplate.from_template(
    """
You are an intelligent routing agent. Based on the user's input below, determine the action they are requesting.

User input:
{input}

Return a JSON object with the following keys:
- "action": (e.g., "respond", "fetch_data", "analyze")
- "ticker": (e.g., "AAPL", "TSLA", etc. — optional, include only if relevant)

Respond ONLY with the JSON object.
"""
)