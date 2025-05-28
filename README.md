# 🧠 Interactive Application with a Local Language Model

## 🚀 What Is This?

Welcome to the world of AI – this time featuring a clever brain: **Qwen3 1.7B**, running locally via **[Ollama](https://ollama.com)**. This project shows how to get a language model to click buttons in a Java GUI based on your text input.

Type something like *"Please press the yellow button"* – and it’ll figure it out and press it.

---

## ⚙️ How It Works

1. **💻 Java GUI**  
   Three buttons: Red, Blue, Yellow. You enter a sentence, the model thinks briefly, and clicks the matching button.

2. **🧠 LLM with Ollama (Qwen3 1.7B)**  
   No external cloud service – just **Qwen3** running locally with **Ollama**, a lightweight tool that makes using LLMs offline easy and fast.

3. **🐍 Python MCP Server (`mcp_server.py`)**  
   The decision-maker. It talks directly to Ollama, analyzes the model's output, and clicks the right button based on the color it finds.

---

## 🛠️ What You Need

### 📅 1. Install Ollama

If you haven’t heard of Ollama, think of it like *Docker for AI models* – but with a turbo button.

👉 [Download Ollama](https://ollama.com/download)

Check if it's working:

```bash
ollama --version
```

### 🧠 2. Get the Qwen3 1.7B Model

Pull the model into your local Ollama setup:

```bash
ollama pull qwen3:1.7b
```

You can try other models too, but this project was made for `qwen3:1.7b` – so stick with it to start.

### 🐍 3. Install Python Requirements

Open your terminal in the project folder and run:

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

**Windows:**
```bash
pip install -r requirements.txt
```

---

## ☕ Starting the Java App

Once Ollama is running and the model is loaded, the Java app takes over. It automatically starts the MCP server and connects to the model.

No need to run extra scripts manually.

---

## ✨ Using It

1. Start the Java application.
2. Enter something like *"Press the red button, please."*
3. The model processes your request.
4. The correct button gets clicked.
5. You'll see the feedback in the GUI.

💡 You can get creative too:  
*"I’m feeling blue – hit that button!"* works just fine.

---

## ⚠️ Notes & Tips

- **Ollama must be running** before starting the Java app.
- You only need to run `ollama pull qwen3:1.7b` once – the model stays available locally.
- **Windows users:**  
  - In the Java code (lines 102 & 108), replace `python3` with `python`, or the script won’t run properly.

---

## 🛠️ Troubleshooting

- **GUI starts, but nothing happens?**  
  → Check if Ollama is running and the model is loaded. If the terminal says "No model found," run `ollama pull qwen3:1.7b`.

- **Weird model replies?**  
  → Use simple color names in your input. "Pitch black" might confuse the model – and there’s no black button anyway 😉.

- **Port issues?**  
  → The MCP server runs on port `5006`. Make sure it's not in use (some IDEs or Jupyter can cause conflicts).

---

## 🧪 Conclusion

With **Ollama** and **Qwen3**, you get a slick, offline setup to add intelligent interaction to your Java GUI. No cloud, no API keys – just install, run, and talk to your app. ✨
