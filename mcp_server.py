from flask import Flask, request, jsonify
import requests
import uuid

# Flask-App erstellen
app = Flask(__name__)
sessions = {}  # Speichert die Sessions, um Benutzeranfragen zu verfolgen

# Funktion zur Verarbeitung des Prompts und der Antwort des GPT-Servers
def process_prompt(session_id, user_prompt, context):
    try:
        # Anfrage an den GPT-Neo-Server senden
        response = requests.post("http://localhost:5002/generate", json={"prompt": user_prompt})
        response.raise_for_status()  # Prüfen, ob der HTTP-Request erfolgreich war
        result = response.json()
        text = result.get("response", "").lower()

        # Liste der Farben, die erkannt werden sollen
        farben = ["rot", "blau", "gelb"]
        erkannte_farbe = None

        # Überprüfen, ob eine Farbe im Text enthalten ist
        for farbe in farben:
            if farbe in text:
                erkannte_farbe = farbe
                break

        # Die Aktion basierend auf der erkannten Farbe festlegen
        if erkannte_farbe:
            action = {
                "action": "click_button",
                "target": erkannte_farbe,
                "confidence": 0.9,
                "explanation": f"'{erkannte_farbe}' erkannt im LLM-Output.",
            }
        else:
            action = {
                "action": "no_action",
                "message": "Keine bekannte Farbe erkannt.",
                "llm_output": text,
            }

        # Session-Informationen speichern
        sessions[session_id]["last_prompt"] = user_prompt
        sessions[session_id]["last_action"] = action

        return action
    except requests.exceptions.RequestException as e:
        # Fehlerbehandlung, falls beim Anrufen des GPT-Servers ein Problem auftritt
        print(f"Fehler beim Aufrufen des GPT-Neo-Servers: {e}")
        return {"action": "error", "message": f"Fehler beim Aufrufen des GPT-Neo-Servers: {e}"}

# MCP-Server-Handler für POST-Anfragen
@app.route('/mcp_request', methods=['POST'])
def mcp_handler():
    try:
        # Session-ID holen oder eine neue generieren
        session_id = request.form.get("session_id") or str(uuid.uuid4())
        if session_id not in sessions:
            sessions[session_id] = {}

        # Benutzerprompt und Kontext aus der Anfrage holen
        user_prompt = request.form.get("user_prompt", "")
        context = request.form.get("context", "")

        # Wenn kein Prompt übergeben wurde, Fehler werfen
        if not user_prompt:
            raise ValueError("Fehlender 'user_prompt' Parameter")

        # Prompt verarbeiten und Antwort zurückgeben
        result = process_prompt(session_id, user_prompt, context)

        return jsonify({
            "session_id": session_id,
            "response": result
        })

    except Exception as e:
        # Fehlerbehandlung für den MCP-Server
        print(f"Fehler im MCP-Server: {e}")
        return jsonify({"error": str(e)}), 500

# Starten des Servers
if __name__ == '__main__':
    print("✅ MCP-Server läuft auf Port 5001 mit Session- und Action-Handling")
    app.run(port=5001)