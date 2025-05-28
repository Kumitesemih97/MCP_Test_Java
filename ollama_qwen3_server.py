from flask import Flask, request, jsonify
import requests  # For sending requests to the Ollama server

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:1.7b"  # This is the model name used by Ollama

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False  # Disable streaming – we want a single response
    }

    # Send the request to the Ollama server
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        generated = response.json().get("response", "")
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"response": generated})

if __name__ == "__main__":
    app.run(port=5005)