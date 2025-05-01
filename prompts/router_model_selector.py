from langchain_core.prompts import ChatPromptTemplate

model_selector_prompt = ChatPromptTemplate.from_template(
    """
You are an intelligent model selector. Based on the user input below,
decide which LLM model is more appropriate to handle the request: "openai" or "gemini".

User input:
{input}

Return ONLY "openai" or "gemini".
"""
)
