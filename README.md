# 🧠 Interaktive Anwendung mit LLM (Language Model)

## 🚀 Was ist das hier eigentlich?

Willkommen in der Welt der KI! Diesmal mit einem besonders schlauen Kopf: **Qwen3 1.7B**, lokal ausgeführt über **[Ollama](https://ollama.com)**. Dieses Projekt zeigt dir, wie du ein Language Model so zähmst, dass es per Texteingabe Buttons in einer Java-GUI klickt. Jep, das ist so nerdig und cool, wie es klingt.

Du schreibst z. B. *"Drück bitte den gelben Button"* und das System denkt nicht lange nach, sondern klickt los. Fast so, als hätte deine Tastatur plötzlich Finger bekommen.

---

## ⚙️ Wie das Ganze läuft

1. **💻 Java-GUI**  
   Drei Buttons: Rot, Blau, Gelb. Du gibst einen Text ein, das LLM denkt kurz nach und drückt den passenden Button.  

2. **🧠 LLM mit Ollama (Qwen3 1.7B)**  
   Statt einem externen Server läuft jetzt **Qwen3** lokal über **Ollama** eine super einfache Möglichkeit, LLMs lokal zu nutzen (keine Cloud, keine Panik, alles offline).  

3. **🐍 Python MCP-Server (`mcp_server.py`)**  
   Der gute alte Entscheidungsserver bleibt erhalten, nur dass er jetzt direkt mit Ollama spricht. Er analysiert den Modell-Output und klickt auf Basis der gefundenen Farbe den richtigen Button.

---

## 🛠️ Vorbereitung: Was du brauchst

### 📅 1. Installiere Ollama

Falls du Ollama noch nicht kennst, es ist quasi *Docker für KI-Modelle*, aber mit einem Turbo-Knopf.

👉 [Download Ollama](https://ollama.com/download)

Nach der Installation kannst du überprüfen, ob alles läuft:

```bash
ollama --version
```

Wenn das klappt, weiter mit Schritt 2.

---

### 🧠 2. Qwen3 1.7B Modell herunterladen

Einmal das Modell in die Ollama-Welt holen:

```bash
ollama pull qwen3:1.7b
```

Du kannst auch andere Modelle probieren, aber dieses Projekt wurde auf `qwen3:1.7b` abgestimmt, also bleib am besten erstmal dabei.

---

### 🐍 3. Python-Abhängigkeiten installieren

Öffne ein Terminal im Projektordner und installiere die notwendigen Pakete:

**macOS/Linux:**
```bash
pip3 install -r requirements.txt
```

**Windows:**
```bash
pip install -r requirements.txt
```

---

## ☕ Die Java-Anwendung starten

Sobald Ollama läuft und das Modell bereitsteht, übernimmt die Java-Anwendung den Rest. Beim Start öffnet sie automatisch den MCP-Server, der mit Ollama spricht. Keine Extra-Server-Skripte nötig.

---

## ✨ Benutzung

1. Starte die Java-Anwendung.
2. Gib einen Satz wie `"Bitte drück den roten Button"` ein.
3. Das Modell interpretiert deine Eingabe.
4. Der Button mit der entsprechenden Farbe wird geklickt.
5. Du bekommst visuelles Feedback direkt in der GUI.

💡 Tipp: Das funktioniert auch mit natürlichsprachlichen Formulierungen wie:  
*"Ich mag Blau, klick den Button bitte."*

---

## ⚠️ Hinweise & Tipps

- Achte darauf, dass **Ollama im Hintergrund läuft**, bevor du die Java-Anwendung startest.
- Das Modell `qwen3:1.7b` muss einmalig mit `ollama pull` heruntergeladen werden – danach bleibt es lokal verfügbar.
- Wenn du unter Windows arbeitest:  
  **Pass im Java-Code Zeile 102 und 108 an – `python3` ➔ `python`**, sonst startet das Skript nicht richtig.

---

## 🛠️ Fehlerbehebung

- **Java-GUI startet, aber nix passiert?**  
  → Läuft Ollama? Modell geladen? Terminal sagt was von "No model found"? Dann hast du vermutlich `ollama pull qwen3:1.7b` vergessen.

- **Modell antwortet nicht sinnvoll?**  
  → Achte auf einfache Farbangaben in deinen Prompts. "Tiefschwarz" versteht das Modell vielleicht nicht als `"schwarz"` (und Schwarz ist hier eh kein Button 😉).

- **Ports blockiert?**  
  → Standardmäßig läuft der MCP-Server auf Port `5001`. Achte darauf, dass nix anderes den Port blockiert (manche IDEs oder Jupyter-Instanzen sind hier gern Spielverderber).

---

## 🧪 Fazit

Mit **Ollama + Qwen** hast du ein elegantes, lokales LLM-Setup, das dir eine smarte Interaktion mit deiner Java-GUI ermöglicht, ganz ohne Cloud, Registrierung oder API-Schlüssel. Einfach: installieren, starten, prompten. ✨

Wenn du Lust auf mehr hast: Denk mal über Sprachsteuerung, Voice2Text oder weiterführende Aktionen nach. Dieses Setup ist ein großartiger Einstiegspunkt!
