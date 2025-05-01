from langchain_core.runnables import RunnableLambda, RunnableBranch, RunnableMap
from router.router_chain import router_chain
from tools.calculator_tool import calculate
from tools.edgar_tool import fetch_edgar_data
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import get_gemini_model, get_openai_model
from prompts.investment_prompt import get_explanation_prompt
from prompts.router_model_selector import model_selector_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

# Models
gemini = get_gemini_model()
openai = get_openai_model()
parser = StrOutputParser()

# Default prompt
default_prompt = PromptTemplate.from_template("{input}")

# Agentic LLM selector
def choose_model_and_prompt(input_data: str, override: str = None):
    """Select model using override or agentic reasoning."""
    if override == "openai":
        print("🔁 Override model: OpenAI selected")
        return openai, get_explanation_prompt()
    elif override == "gemini":
        print("🔁 Override model: Gemini selected")
        return gemini, get_explanation_prompt()

    # Use Gemini to select model based on content
    router_response = gemini.invoke(model_selector_prompt.format(input=input_data))
    selected = parser.invoke(router_response.content.strip().lower())

    if "openai" in selected:
        print("🤖 Agentic router chose OpenAI based on input")
        return openai, get_explanation_prompt()
    else:
        print("🤖 Agentic router chose Gemini based on input")
        return gemini, get_explanation_prompt()

# Dynamic LLM response chain with override logic
def dynamic_llm_chain(input_data: dict):
    input_text = input_data.get("llm_input", input_data.get("input"))
    override = input_data.get("override")
    model, prompt = choose_model_and_prompt(input_text, override)
    return StrOutputParser().invoke(model.invoke(prompt.format(summary=input_text, recommendation="")).content)

# Tool wrappers
def calculator_tool_wrapper(input_data):
    expression = input_data.get("input") if isinstance(input_data, dict) else input_data
    if not expression:
        return "⚠️ Error: no input provided for calculation."
    try:
        return f"🧮 Result: {eval(expression)}"
    except Exception as e:
        return f"❌ Calculation error: {e}"

def edgar_tool_wrapper(input_data):
    ticker = input_data.get("input") if isinstance(input_data, dict) else input_data
    return fetch_edgar_data(ticker)

# Action condition checks
def is_calculate_action(x): return isinstance(x, dict) and x.get("action") == "calculate"
def is_respond_action(x): return isinstance(x, dict) and x.get("action") == "respond"
def is_edgar_action(x): return isinstance(x, dict) and x.get("action") == "edgar"

# Final router with branching logic
router = (
    router_chain
    | RunnableMap({
        "input": lambda x: x.get("input"),
        "llm_input": lambda x: x.get("input"),
        "action": lambda x: x.get("action"),
        "override": lambda x: x.get("override", None)
    })
    | RunnableBranch(
        (is_calculate_action, RunnableLambda(calculator_tool_wrapper)),
        (is_edgar_action, RunnableLambda(edgar_tool_wrapper)),
        (is_respond_action, RunnableLambda(dynamic_llm_chain)),
        RunnableLambda(lambda _: "🤖 Sorry, I didn't understand your request.")
    )
)
