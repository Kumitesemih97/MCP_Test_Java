from flask import Flask, request, jsonify
import requests
import uuid
import re

app = Flask(__name__)
sessions = {}

# 📘 Anleitungen für das LLM
def get_tool_instructions():
    return """
Du kannst folgende Funktionen aufrufen:

1. get_button_ids()
   - Gibt eine Liste aller verfügbaren Button-IDs zurück.

2. press_button_by_id()
   - Drückt den im Prompt angegebenen Button.

Antworte immer mit genau einem Funktionsaufruf aus der obigen Liste, z. B.:
get_button_ids()
oder
press_button_id("red_button")

Neben dem Funktionsaufruf kannst du auch erklären, warum du diese Funktion gewählt hast. Schreibe zuerst den Funktionsaufruf in einer eigenen Zeile, gefolgt von einer Leerzeile und dann deinem Reasoning-Text.
"""

# 🎨 Dummy-Buttons – später gerne aus echter GUI generieren
def get_button_ids():
    return ["red_button", "blue_button", "yellow_button"]

# 🖲️ Simulierter Button-Klick
def press_button_by_id(button_id):
    return {
        "action": "press_button",
        "button_id": button_id,
        "message": f"Button '{button_id}' wurde gedrückt."
    }

# 🧠 LLM-Antwort analysieren
def parse_llm_response(text):
    match = re.match(r"(\w+\([^\)]*\))\s*\n\s*\n(.+)", text, re.DOTALL)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    func_match = re.match(r"(\w+\([^\)]*\))", text)
    if func_match:
        return func_match.group(1).strip(), ""

    return None, text  # Wenn nichts erkannt, ist das Ganze vielleicht nur Kommentar

# ⚙️ Prompt verarbeiten, Antwort generieren und passende Aktion auslösen
def process_prompt(session_id, user_prompt, context):
    try:
        full_prompt = f"{get_tool_instructions()}\n\nNutzer: {user_prompt}"

        ollama_payload = {
            "model": "qwen3:1.7b",
            "prompt": full_prompt,
            "stream": False
        }

        response = requests.post("http://localhost:11434/api/generate", json=ollama_payload)
        response.raise_for_status()
        result = response.json()

        llm_text = result.get("response", "").strip()
        print(f"\n🧠 LLM Roh-Antwort:\n{llm_text}\n---")

        func_call, reasoning = parse_llm_response(llm_text.lower())
        print(f"🔍 Gefundener Funktionsaufruf: {func_call}")
        print(f"💡 Reasoning: {reasoning}")

        # 💬 Funktionsaufruf in echte Aktion umsetzen
        action = {"action": "no_action", "message": "Keine bekannte Funktion erkannt.", "llm_output": llm_text}

        if func_call == "get_button_ids()":
            action = {
                "action": "get_button_ids",
                "buttons": get_button_ids(),
                "message": "Liste der verfügbaren Buttons zurückgegeben."
            }
        elif func_call.startswith("press_button_id("):
            button_id_match = re.search(r'press_button_id\(["\']?(\w+)_button["\']?\)', func_call)
            if button_id_match:
                button_id = button_id_match.group(1) + "_button"
                if button_id in get_button_ids():
                    action = press_button_by_id(button_id)

        # 💾 Session-Infos speichern
        sessions.setdefault(session_id, {})
        sessions[session_id].update({
            "last_prompt": user_prompt,
            "last_action": action,
            "last_reasoning": reasoning
        })

        return {
            "function_call": func_call or "",
            "reasoning": reasoning,
            "action_result": action
        }

    except requests.exceptions.RequestException as e:
        print(f"❌ Fehler beim Aufrufen des Ollama-Servers: {e}")
        return {"action": "error", "message": f"Fehler beim Aufrufen des Ollama-Servers: {e}"}

# 🚪 Haupt-Endpunkt für MCP-Client
@app.route('/mcp_request', methods=['POST'])
def mcp_handler():
    try:
        session_id = request.form.get("session_id") or str(uuid.uuid4())
        user_prompt = request.form.get("user_prompt", "")
        context = request.form.get("context", "")

        if not user_prompt:
            raise ValueError("Fehlender 'user_prompt'-Parameter")

        result = process_prompt(session_id, user_prompt, context)

        return jsonify({
            "session_id": session_id,
            "response": result
        })

    except Exception as e:
        print(f"🚨 Fehler im MCP-Server: {e}")
        return jsonify({"error": str(e)}), 500

# 🏁 Los geht's!
if __name__ == '__main__':
    print("✅ MCP-Server läuft auf Port 5006 mit Qwen3:1.7b via Ollama")
    app.run(port=5006)
