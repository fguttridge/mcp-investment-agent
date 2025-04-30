import math
from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the directory containing agent_runner.py to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from router.router_runner import router

app = Flask(__name__)

# Sanitize data to handle NaN values
def sanitize_data(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = sanitize_data(value)  # Recursively sanitize
    elif isinstance(data, list):
        for i in range(len(data)):
            data[i] = sanitize_data(data[i])  # Recursively sanitize
    elif isinstance(data, float) and (math.isnan(data) or data is None):
        return 'N/A'  # Replace NaN with 'N/A'
    return data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # Get the user input from the POST request (JSON body)
    user_input = request.json.get('input')

    if not user_input:
        return jsonify({"error": "Please provide an input."}), 400
    
    # Call the agent's response
    output = router.invoke({"action": "respond", "input": user_input})

    # Sanitize the response to replace NaN with 'N/A'
    sanitized_output = sanitize_data(output)

    return jsonify({"response": sanitized_output})

if __name__ == "__main__":
    app.run(debug=True)