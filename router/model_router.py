from config import get_gemini_model, get_openai_model
from prompts.investment_prompt import get_explanation_prompt
from prompts.router_model_selector import model_selector_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap

# Load models once
gemini = get_gemini_model()
openai = get_openai_model()

# Parser for clean string output
parser = StrOutputParser()

# Model selection chain (agentic) using OpenAI for reasoning
model_selection_chain = (
    RunnableMap({"input": lambda x: x})
    | model_selector_prompt
    | openai  # You can switch to gemini if preferred
    | parser
)

def choose_model_and_prompt(input_data: str, override: str = None):
    """
    Uses agentic routing to choose the best LLM and prompt combo,
    with optional manual override from dropdown.
    """

    if override == "openai":
        print("🔁 Override model: OpenAI selected")
        return openai, get_explanation_prompt()
    elif override == "gemini":
        print("🔁 Override model: Gemini selected")
        return gemini, get_explanation_prompt()

    # Agentic routing
    try:
        selected_model = model_selection_chain.invoke(input_data).strip().lower()
    except Exception as e:
        print(f"⚠️ Model selection failed: {e}")
        selected_model = "gemini"  # Fallback

    if "openai" in selected_model:
        print("🤖 Agentic router chose OpenAI based on input")
        return openai, get_explanation_prompt()
    else:
        print("🤖 Agentic router chose Gemini based on input")
        return gemini, get_explanation_prompt()