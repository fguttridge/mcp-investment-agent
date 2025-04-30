from langchain_core.runnables import RunnableLambda, RunnableBranch, RunnableMap
from router.router_chain import router_chain
from tools.calculator_tool import calculate
from tools.edgar_tool import fetch_edgar_data 
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from config import get_gemini_model

# Initialize LLM (for regular responses)
llm = get_gemini_model()

# Define the default prompt for regular replies (Gemini model)
default_prompt = PromptTemplate.from_template("{input}")
default_chain = default_prompt | llm | StrOutputParser()

def add_input_to_output(data):
    """Merges parsed output and input for consistency in the response"""
    return {
        **data["parsed_output"],
        "input": data["input"]
    }

# Define the calculator tool wrapper
def calculator_tool_wrapper(input_data):
    expression = input_data.get("input") if isinstance(input_data, dict) else input_data
    if not expression:
        return "⚠️ Error: no input provided for calculation."

    try:
        # Evaluate the expression (use safer methods like sympy if needed)
        result = eval(expression)
        return f"🧮 Result: {result}"
    except Exception as e:
        return f"❌ Calculation error: {e}"
    
def edgar_tool_wrapper(input_data):
    ticker = input_data.get("input") if isinstance(input_data, dict) else input_data
    return fetch_edgar_data(ticker)

# Clean condition checkers to identify the type of request (calculate/respond)
def is_calculate_action(x):
    """Returns True if the action is 'calculate'"""
    return isinstance(x, dict) and x.get("action") == "calculate"

def is_respond_action(x):
    """Returns True if the action is 'respond'"""
    return isinstance(x, dict) and x.get("action") == "respond"

def is_edgar_action(x):
    return isinstance(x, dict) and x.get("action") == "edgar"

# Router Chain Logic - handling both calculation and default responses
router = (
    router_chain  # This chain should output a dict with {"action": "...", "input": "..."}
    | RunnableMap({
        "input": lambda x: x["input"] if isinstance(x, dict) else x,  # Ensure input is passed correctly
        "llm_input": lambda x: str(x["input"]) if isinstance(x, dict) else str(x),  # Pass input as string to LLM
        "action": lambda x: str(x["action"]) if isinstance(x, dict) else str(x) # Retain the action for subsequent checks
    })
    | RunnableBranch(
        (is_calculate_action, RunnableLambda(calculator_tool_wrapper)),
        (is_edgar_action, RunnableLambda(edgar_tool_wrapper)),  # For calculate actions
        (is_respond_action, default_chain),  # Default response chain
        RunnableLambda(lambda _: "🤖 Sorry, I didn't understand your request.")  # Fallback response
    )
)
