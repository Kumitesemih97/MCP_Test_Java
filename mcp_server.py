from flask import Flask, request, jsonify
import requests
import uuid
import re

app = Flask(__name__)
sessions = {}

# 📘 Instructions for the LLM
def get_tool_instructions():
    return """
You can call the following functions:

1. get_button_ids()
   - Returns a list of all available button IDs.

2. press_button_by_id()
   - Presses the button specified in the prompt.

If the user asks to press a button and you already know the button's ID (e.g., 'red_button', 'blue_button', 'yellow_button'), call press_button_by_id() directly with the correct ID. Only call get_button_ids() if you do NOT know the button's ID.

Always respond with exactly one function call from the list above, e.g.:
press_button_by_id("red_button")

Write the function call on a new line, followed by an empty line and then your reasoning text.
"""

# 🎨 Dummy buttons – ideally generated from the actual GUI later
def get_button_ids():
    return ["red_button", "blue_button", "yellow_button"]

# 🖲️ Simulated button press
def press_button_by_id(button_id):
    return {
        "action": "press_button",
        "button_id": button_id,
        "message": f"Button '{button_id}' was pressed."
    }

# 🧠 Analyze LLM response
def parse_llm_response(text):
    match = re.match(r"(\w+\([^\)]*\))\s*\n\s*\n(.+)", text, re.DOTALL)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    func_match = re.match(r"(\w+\([^\)]*\))", text)
    if func_match:
        return func_match.group(1).strip(), ""

    return None, text  # If nothing recognized, it's probably just a comment

# ⚙️ Process prompt, generate response, and trigger appropriate action
def process_prompt(session_id, user_prompt, context):
    try:
        full_prompt = f"{get_tool_instructions()}\n\nUser: {user_prompt}"

        ollama_payload = {
            "model": "qwen3:1.7b",
            "prompt": full_prompt,
            "stream": False
        }

        # First LLM call
        response = requests.post("http://localhost:5005/generate", json=ollama_payload)
        response.raise_for_status()
        result = response.json()
        llm_text = result.get("response", "").strip()
        func_call, reasoning = parse_llm_response(llm_text.lower())

        # If the LLM calls get_button_ids(), do a follow-up turn
        if func_call == "get_button_ids()":
            button_info = {
                "red_button": "red (medium brightness)",
                "blue_button": "blue (dark)",
                "yellow_button": "yellow (brightest)"
            }
            button_list = "\n".join([f"- {k}: {v}" for k, v in button_info.items()])
            followup_prompt = (
                f"{get_tool_instructions()}\n\n"
                f"User: {user_prompt}\n"
                f"Assistant: get_button_ids()\n\n"
                f"Available buttons:\n"
                f"{button_list}\n"
                f"Now, please press the correct button."
            )
            ollama_payload["prompt"] = followup_prompt
            response2 = requests.post("http://localhost:5005/generate", json=ollama_payload)
            response2.raise_for_status()
            result2 = response2.json()
            llm_text2 = result2.get("response", "").strip()
            func_call2, reasoning2 = parse_llm_response(llm_text2.lower())
            func_call = func_call2
            reasoning = reasoning2

        # Map function call to real action
        action = {"action": "no_action", "message": "No recognized function.", "llm_output": llm_text}
        if func_call == "get_button_ids()":
            action = {
                "action": "get_button_ids",
                "buttons": ["red_button", "blue_button", "yellow_button"],
                "message": "Returned list of available buttons."
            }
        elif func_call is not None and func_call.startswith("press_button_by_id("):
            button_id_match = re.search(r'press_button_by_id\(["\']?(\w+_button)["\']?\)', func_call)
            if button_id_match:
                button_id = button_id_match.group(1)
                if button_id in ["red_button", "blue_button", "yellow_button"]:
                    action = press_button_by_id(button_id)

        # Save session info
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
        print(f"❌ Error calling Ollama server: {e}")
        return {"action": "error", "message": f"Error calling Ollama server: {e}"}

# 🚪 Main endpoint for MCP client
@app.route('/mcp_request', methods=['POST'])
def mcp_handler():
    try:
        session_id = request.form.get("session_id") or str(uuid.uuid4())
        user_prompt = request.form.get("user_prompt", "")
        context = request.form.get("context", "")

        if not user_prompt:
            raise ValueError("Missing 'user_prompt' parameter")

        result = process_prompt(session_id, user_prompt, context)

        return jsonify({
            "session_id": session_id,
            "response": result
        })

    except Exception as e:
        print(f"🚨 Error in MCP server: {e}")
        return jsonify({"error": str(e)}), 500

# 🏁 Let's go!
if __name__ == '__main__':
    print("✅ MCP server running on port 5006 with Qwen3:1.7b via Ollama")
    app.run(port=5006)