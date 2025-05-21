from flask import Flask, request, jsonify
import requests
import uuid
import re

app = Flask(__name__)
sessions = {}

def get_tool_instructions():
    return """
Du kannst folgende Funktionen aufrufen:

1. get_button_ids()
   - Gibt eine Liste aller verfügbaren Button-IDs zurück.

2. press_button_id()
   - Drückt den im Prompt angegebenen Button.

Antworte immer mit genau einem Funktionsaufruf aus der obigen Liste, z.B.:
get_button_ids()
oder
press_button_id()

Neben dem Funktionsaufruf kannst du auch erklären, warum du diese Funktion gewählt hast. Schreibe zuerst den Funktionsaufruf in einer eigenen Zeile, gefolgt von einer Leerzeile und dann deinem Reasoning-Text.
"""

# Simulierte Button-IDs, kann an GUI angepasst werden
def get_button_ids():
    return ["red_button", "blue_button", "yellow_button"]

# Beispielhafte Button-Press-Handler
def press_button_by_id(button_id):
    # Hier solltest du die tatsächliche Logik implementieren, z.B. Event an Java GUI senden
    return {
        "action": "press_button",
        "button_id": button_id,
        "message": f"Button '{button_id}' wurde gedrückt."
    }

# LLM-Antwort parsen: Funktion und Reasoning trennen
def parse_llm_response(text):
    # Beispiel: "press_red_button()\n\nIch denke, Rot ist gemeint, weil..."
    match = re.match(r"(\w+\([^\)]*\))\s*\n\s*\n(.+)", text, re.DOTALL)
    if match:
        func_call = match.group(1).strip()
        reasoning = match.group(2).strip()
        return func_call, reasoning
    else:
        # Wenn keine Trennung, schauen wir ob nur Funktionsaufruf
        func_call_only_match = re.match(r"(\w+\([^\)]*\))", text)
        if func_call_only_match:
            return func_call_only_match.group(1).strip(), ""
    return None, text  # Falls nichts erkannt, ganzes als Reasoning

def process_prompt(session_id, user_prompt, context):
    try:
        # Tool-Anleitung und Kontext + Nutzerprompt zusammensetzen
        full_prompt = get_tool_instructions() + "\n\nNutzer: " + user_prompt

        ollama_payload = {
            "model": "qwen3:4b",
            "prompt": full_prompt,
            "stream": False
        }

        response = requests.post("http://localhost:11434/api/generate", json=ollama_payload)
        response.raise_for_status()
        result = response.json()

        # Das gesamte Antwortfeld aus dem Modell (z.B. "response")
        llm_text = result.get("response", "").strip()
        print(f"LLM Roh-Antwort:\n{llm_text}\n---")

        func_call, reasoning = parse_llm_response(llm_text.lower())

        print(f"Gefundener Funktionsaufruf: {func_call}")
        print(f"Reasoning: {reasoning}")

        # Mapping Funktionsaufrufe auf Aktionen
        if func_call == "get_button_ids()":
            buttons = get_button_ids()
            action = {
                "action": "get_button_ids",
                "buttons": buttons,
                "message": "Liste der verfügbaren Buttons zurückgegeben."
            }
        elif func_call == "press_red_button()":
            action = press_button_by_id("red_button")
        elif func_call == "press_blue_button()":
            action = press_button_by_id("blue_button")
        elif func_call == "press_yellow_button()":
            action = press_button_by_id("yellow_button")
        else:
            action = {
                "action": "no_action",
                "message": "Keine bekannte Funktion erkannt.",
                "llm_output": llm_text
            }

        # Session-Infos speichern
        if session_id not in sessions:
            sessions[session_id] = {}
        sessions[session_id]["last_prompt"] = user_prompt
        sessions[session_id]["last_action"] = action
        sessions[session_id]["last_reasoning"] = reasoning

        # Rückgabe an Client: Aktion + Reasoning
        return {
            "function_call": func_call or "",
            "reasoning": reasoning,
            "action_result": action
        }

    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Aufrufen des Ollama-Servers: {e}")
        return {"action": "error", "message": f"Fehler beim Aufrufen des Ollama-Servers: {e}"}

@app.route('/mcp_request', methods=['POST'])
def mcp_handler():
    try:
        session_id = request.form.get("session_id") or str(uuid.uuid4())
        if session_id not in sessions:
            sessions[session_id] = {}

        user_prompt = request.form.get("user_prompt", "")
        context = request.form.get("context", "")

        if not user_prompt:
            raise ValueError("Fehlender 'user_prompt' Parameter")

        result = process_prompt(session_id, user_prompt, context)

        return jsonify({
            "session_id": session_id,
            "response": result
        })

    except Exception as e:
        print(f"Fehler im MCP-Server: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("✅ MCP-Server läuft auf Port 5006 mit Qwen3:4b via Ollama")
    app.run(port=5006)
