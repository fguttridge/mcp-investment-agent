from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_google_genai import ChatGoogleGenerativeAI
from router.router_prompt import router_prompt
import config
import os
from dotenv import load_dotenv

load_dotenv()

# Get the LLM model (Google Gemini or other)
llm = config.get_gemini_model()

# JSON parser for parsing the model's output
parser = JsonOutputParser()

# ✅ Safe merging function for output
def add_input_to_output(data):
    return {
        **(data.get("parsed_output", {}) if isinstance(data.get("parsed_output"), dict) else {}),
        "input": data.get("input", "No input provided")
    }

# Chain: input → prompt → Gemini → JSON → combine with original input
router_chain = (
    RunnableMap({
        "input": lambda x: x["input"] if isinstance(x, dict) else str(x),
    })
    | RunnableMap({
        "parsed_output": lambda x: parser.invoke(
            llm.invoke(router_prompt.format(input=x["input"])).content
        ),
        "input": lambda x: x["input"],
    })
    | RunnableLambda(lambda data: {
        "action": data["parsed_output"].get("action"),
        "input": data["parsed_output"].get("ticker") if "ticker" in data["parsed_output"] else data.get("input", "No input provided")
    })
)
