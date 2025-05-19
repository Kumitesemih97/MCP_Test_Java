from flask import Flask, request, jsonify
import requests  # Um Anfragen an den Ollama-Server zu senden

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3:1.7b"  # So lautet der Modellname bei Ollama

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False  # Kein Streaming, wir wollen eine einfache Antwort
    }

    # Anfrage an den Ollama-Server
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        generated = response.json().get("response", "")
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"response": generated})

if __name__ == "__main__":
    app.run(port=5005)
