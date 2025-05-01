from flask import Flask, render_template, request, jsonify
from router.router_runner import router
import math

app = Flask(__name__)

def sanitize_data(data):
    if isinstance(data, dict):
        return {k: sanitize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(i) for i in data]
    elif isinstance(data, float) and (math.isnan(data) or data is None):
        return 'N/A'
    return data

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_input = data.get("input")
    model_override = data.get("model_override")  # ✅ Capture override

    if not user_input:
        return jsonify({"error": "Please provide an input."}), 400

    print(f"📨 Received input: {user_input}")
    print(f"🎛️ Override mode: {model_override}")
    try:
        result = router.invoke({
            "action": "respond",
            "input": user_input,
            "model_override": model_override
        })
        print(f"✅ Final Output: {result}")
        return jsonify({"response": sanitize_data(result)})
    
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)