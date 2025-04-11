import os
import subprocess
from transformers import AutoTokenizer, AutoModelForCausalLM

def install_requirements():
    print("Überprüfe, ob alle erforderlichen Pakete installiert sind...")
    
    # Installiere torch und transformers, falls noch nicht installiert
    try:
        import torch
        import transformers
        print("Alle notwendigen Pakete sind bereits installiert.")
    except ImportError:
        print("Einige Pakete fehlen, installiere sie jetzt...")
        subprocess.check_call([os.sys.executable, "-m", "pip", "install", "torch", "transformers"])

def download_model():
    model_name = "EleutherAI/gpt-neo-125M"
    print(f"Lade {model_name} von Hugging Face herunter...")

    try:
        # Tokenizer und Modell herunterladen
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        print(f"Modell '{model_name}' erfolgreich heruntergeladen und gespeichert!")
    except Exception as e:
        print(f"Fehler beim Herunterladen des Modells: {str(e)}")
        raise

def main():
    install_requirements()
    download_model()

if __name__ == "__main__":
    main()