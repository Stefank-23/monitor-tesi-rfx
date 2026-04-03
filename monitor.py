import requests
from bs4 import BeautifulSoup
import os

# 1. RECUPERO CREDENZIALI (DA GITHUB SECRETS)
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# 2. URL DI TEST (WIKIPEDIA)
# Usiamo Wikipedia perché è stabile e non blocca gli script
URL = "https://it.wikipedia.org/wiki/Energia_nucleare"

def invia_telegram(messaggio):
    """Invia il messaggio in formato testo semplice per evitare errori 400."""
    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": messaggio  # Rimosso parse_mode per sicurezza
    }
    try:
        r = requests.post(url_tg, data=payload)
        if r.status_code != 200:
            print(f"Errore Telegram {r.status_code}: {r.text}")
        else:
            print("Messaggio inviato con successo!")
    except Exception as e:
        print(f"Errore invio Telegram: {e}")

def controlla():
    """Funzione principale di scraping e monitoraggio."""
    tesi_attuali = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"Avvio scansione su: {URL}")
        # Per Wikipedia non usiamo il proxy (non serve), facciamo una richiesta diretta
        response = requests.get(URL, headers=headers, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cerchiamo i titoli dei paragrafi (h2 e h3)
            for elemento in soup.find_all(['h2', 'h3']):
                testo = elemento.get_text().strip()
                testo_low = testo.lower()
                
                # Filtro di test: cerchiamo termini legati al nucleare
                if len(testo) > 5:
                    if any(p in testo_low for p in ["nucleare", "reattore", "fissione", "fusione"]):
                        if testo not in tesi_attuali:
                            tesi_attuali.append(testo)
                            print(f"DEBUG - Trovato: {testo}")

            # GESTIONE STORICO (tesi_viste.txt)
            file_storico = "tesi_viste.txt"
            if os.path.exists(file_storico):
                with open(file_storico, "r", encoding="utf-8") as f:
                    viste = f.read().splitlines()
            else:
                viste = []

            # IDENTIFICA LE NOVITÀ
            nuove = [t for t in tesi_attuali if t not in viste]

            if nuove:
                # Creiamo il messaggio per Telegram
                messaggio = "🧪 *TEST WIKIPEDIA FUNZIONANTE!*\n\n"
                messaggio += "Lo script ha letto correttamente la pagina. Ecco cosa ha trovato:\n"
                for n in nuove:
                    messaggio += f"• {n}\n"
                
                invia_telegram(messaggio)
                
                # Aggiorniamo il file storico per non reinviare tutto la prossima volta
                with open(file_storico, "a", encoding="utf-8") as f:
                    for n in nuove:
                        f.write(n + "\n")
                print(f"Inviate {len(nuove)} novità su Telegram.")
            else:
                print("Nessuna novità trovata (titoli già presenti nello storico).")
        else:
            print(f"Il sito ha risposto con codice: {response.status_code}")

    except Exception as e:
        print(f"Errore durante lo scraping: {e}")

if __name__ == "__main__":
    # Verifica che i Secrets siano caricati
    if not TOKEN or not CHAT_ID:
        print("ERRORE: Secrets TELEGRAM_TOKEN o TELEGRAM_CHAT_ID non configurati!")
    else:
        controlla()
