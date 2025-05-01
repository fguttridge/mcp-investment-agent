from router.router_chain import router_chain

# Test inputs
test_inputs = [
    {"input": "Summarize the 10-K filing for AAPL"},
    {"input": "Should I invest in NVIDIA right now?"},
    {"input": "Provide a financial analysis of Tesla's latest earnings"},
    {"input": "Compare Google's growth with Microsoft"},
]

# Run test
for i, user_input in enumerate(test_inputs, start=1):
    print(f"\n🧪 Test {i}: Input = {user_input['input']}")
    result = router_chain.invoke(user_input)
    print("✅ Result:", result)
