from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_core.output_parsers import JsonOutputParser
from router.model_router import choose_model_and_prompt
from prompts.router_prompt import router_prompt
import json

parser = JsonOutputParser()

def model_and_prompt_router(data):
    input_text = data["input"]
    override = data.get("model_override")
    print(f"Ἆ router_chain - input_text: {input_text}, override: {override}")
    model, _ = choose_model_and_prompt(input_text, override=override)
    llm_response = model.invoke(router_prompt.format(input=input_text)).content
    print(f"📦 Raw LLM Output: {llm_response}")
    try:
        parsed = parser.invoke(llm_response)
        print(f"🔢 Parsed Output: {parsed}")
        return parsed
    except Exception as e:
        print(f"❌ JSON parsing error: {e}")
        return {"action": "unknown", "input": input_text}

router_chain = (
    RunnableMap({
        "input": lambda x: x["input"],
        "model_override": lambda x: x.get("model_override"),
    }) | RunnableMap({
        "parsed_output": model_and_prompt_router,
        "input": lambda x: x["input"]
    }) | RunnableLambda(lambda data: (
        lambda parsed: {
            "action": parsed.get("action", "unknown"),
            "input": parsed.get("ticker") or data.get("input", "No input")
        }
    )(json.loads(data["parsed_output"]) if isinstance(data["parsed_output"], str) else data["parsed_output"]))
)
