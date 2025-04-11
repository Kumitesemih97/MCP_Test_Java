
# Interaktive Anwendung mit LLM (Language Model)

## Überblick

Dieses Projekt ermöglicht eine interaktive Benutzeroberfläche (GUI) mit einem Language Model (LLM), das in der Lage ist, basierend auf Benutzereingaben bestimmte Aktionen auszuführen. Im Speziellen wird das Modell auf Farben reagieren, und bei der Eingabe von Farbnamen durch den Benutzer wird der passende Button in der GUI geklickt. Zusätzlich wird der Zustand des Buttons geändert, um dem Benutzer anzuzeigen, dass die Aktion erfolgreich war.

## Funktionsweise

1. **Java GUI**: Die GUI enthält Buttons für verschiedene Farben (Rot, Blau, Gelb). Der Benutzer kann einen Text eingeben, der das Modell auffordert, eine Farbe zu erkennen.
2. **Python Server (gpt_neo_server.py)**: Dieser Server empfängt Anfragen, generiert Text basierend auf einem Prompt und gibt eine Antwort zurück.
3. **Python Server (mcp_server.py)**: Dieser Server empfängt die generierten Texte vom gpt-neo-server und trifft Entscheidungen, wie etwa das Klicken eines bestimmten Buttons, wenn der Modelloutput eine Farbe enthält.

## Installation

### Abhängigkeiten installieren

Für dieses Projekt müssen einige Python-Abhängigkeiten installiert werden. Benutze dafür den folgenden Befehl. 

**Achtung**: Auf macOS solltest du `pip3` verwenden.

```bash
pip3 install -r requirements.txt
```

Auf Windows solltest du `pip` verwenden:

```bash
pip install -r requirements.txt
```

### LLM-Model herunterladen und installieren

Da das Projekt ein LLM-Modell (GPT-Neo) verwendet, ist es notwendig, dieses Modell lokal herunterzuladen. Dafür stelle ich ein zusätzliches Python-Skript zur Verfügung (`download_llm.py`), das du ausführen kannst, um das Modell zu installieren. 

1. Lade das Skript `download_llm.py` herunter.
2. Führe es mit Python aus, um das Modell zu installieren:

   Auf macOS:
   ```bash
   python3 download_llm.py
   ```
   Auf Windows:
   ```bash
   python download_llm.py
   ```

   Dieses Skript lädt das GPT-Neo Modell herunter und speichert es auf deinem lokalen System.

### Java GUI

Die Java-Anwendung startet automatisch die beiden benötigten Python-Server (`gpt-neo-server.py` und `mcp-server.py`) beim Starten der GUI. Du musst die Server also nicht manuell starten. Alles was du tun musst, ist sicherzustellen, dass die Python-Umgebung korrekt eingerichtet ist und die Dependencies installiert sind.

## Nutzung

1. Starte die Java-Anwendung. Die GUI wird angezeigt, und du kannst mit dem LLM interagieren.
2. Gib einen Text ein, der eine Farbe beschreibt (z. B. "Klicke den blauen Button").
3. Das Modell verarbeitet den Text und der Button, der die erkannte Farbe repräsentiert, wird geklickt.
4. Die Farbe des geklickten Buttons ändert sich und eine Bestätigung wird im GUI angezeigt.

## Wichtige Hinweise

- Stelle sicher, dass Python und alle Abhängigkeiten korrekt installiert sind.
- Auf macOS und Linux wird in der Regel `pip3` verwendet, während auf Windows einfach `pip` verwendet wird.
- Das LLM-Modell wird beim ersten Start der Anwendung automatisch heruntergeladen, wenn es noch nicht lokal vorhanden ist.
- Wenn du die Java-Anwendung unter Windows starten möchtest, ändere im Java-Code in **Zeile 102 und 108** von `python3`auf `python`, um eine fehlerfreie Funktion der Anwendung zu garantieren.

## Fehlerbehebung

- **Fehler beim Starten der Server**: Überprüfe, ob alle Dependencies korrekt installiert sind und dass keine Portkonflikte mit anderen Anwendungen bestehen.
- **Fehler bei der Eingabe**: Achte darauf, dass du einen gültigen Text eingibst, der eine der unterstützten Farben (rot, blau, gelb) enthält.