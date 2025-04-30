# agent_runner.py
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from router.router_runner import router

if __name__ == "__main__":
    while True:
        user_input = input("\n🔎 Ask something (or 'exit'): ")
        if user_input.lower() == "exit":
            break

        # Wrap the input into a dictionary (with 'respond' as the action)
        output = router.invoke({"action": "respond", "input": user_input})  # The action can be either 'respond' or 'calculate'
        print("🤖 Response:", output)