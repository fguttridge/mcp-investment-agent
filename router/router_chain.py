
from langchain_core.runnables import RunnableLambda, RunnableMap
from langchain_core.output_parsers import JsonOutputParser
from router.model_router import choose_model_and_prompt
from prompts.router_prompt import router_prompt

parser = JsonOutputParser()

def model_and_prompt_router(data):
    input_text = data["input"]
    override = data.get("model_override")
    print(f"🧩 router_chain - input_text: {input_text}, override: {override}")
    model, _ = choose_model_and_prompt(input_text, override=override)
    return parser.invoke(model.invoke(router_prompt.format(input=input_text)).content)

router_chain = (
    RunnableMap({
        "input": lambda x: x["input"],
        "model_override": lambda x: x.get("model_override"),
    }) | RunnableMap({
        "parsed_output": model_and_prompt_router,
        "input": lambda x: x["input"]
    }) | RunnableLambda(lambda data: {
        "action": data["parsed_output"].get("action"),
        "input": data["parsed_output"].get("ticker") or data.get("input", "No input")
    })
)
