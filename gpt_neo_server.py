from flask import Flask, request, jsonify  # Flask für die Web-App und JSON-Verarbeitung importieren
from transformers import GPTNeoForCausalLM, AutoTokenizer  # GPT-Neo Modell und Tokenizer importieren
import torch  # PyTorch für Modellverarbeitung importieren (wird hier aber nicht direkt verwendet)

app = Flask(__name__)  # Flask-App starten

# Modell und Tokenizer laden, hier verwenden wir GPT-Neo-125M
model_name = "EleutherAI/gpt-neo-125M"  
tokenizer = AutoTokenizer.from_pretrained(model_name)  # Tokenizer lädt das Modell
model = GPTNeoForCausalLM.from_pretrained(model_name)  # Das GPT-Neo Modell selbst laden

# Route, die POST-Anfragen entgegennimmt und Text generiert
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()  # Holen uns die Daten aus der Anfrage im JSON-Format
    prompt = data.get("prompt", "")  # Den Prompt aus den Daten extrahieren, falls er nicht da ist, leer lassen

    # Den Prompt in Tokens umwandeln, damit das Modell damit arbeiten kann
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Das Modell aufrufen, um eine Antwort basierend auf dem Prompt zu generieren
    outputs = model.generate(**inputs, max_new_tokens=50)  # Hier wird die Ausgabe auf maximal 50 Tokens begrenzt

    # Die Antwort des Modells dekodieren, um den Text zu bekommen
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Den generierten Text als JSON zurückgeben
    return jsonify({"response": generated})

# Den Server starten, wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    app.run(port=5002)  # Die App auf Port 5002 laufen lassen