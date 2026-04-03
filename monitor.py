import requests
from bs4 import BeautifulSoup
import os

# 1. CONFIGURAZIONE (I Secrets rimangono quelli che hai già impostato)
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# URL originale e versione "Proxy" per bypassare i blocchi
URL_ORIGINALE = "https://www.igi.cn/formazione/tesi-di-laurea-magistrale/"
URL_PROXY = f"https://api.allorigins.win/raw?url={URL_ORIGINALE}"

def invia_telegram(messaggio):
    """Invia la notifica definitiva."""
    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": messaggio}
    try:
        r = requests.post(url_tg, data=payload)
        if r.status_code == 200:
            print("Notifica inviata con successo!")
        else:
            print(f"Errore Telegram: {r.text}")
    except Exception as e:
        print(f"Errore invio: {e}")

def controlla():
    tesi_attuali = []
    # Identità per sembrare un browser vero
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"Scansione tesi RFX in corso...")
        # Usiamo il proxy per evitare il Timeout
        response = requests.get(URL_PROXY, headers=headers, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cerchiamo in quasi tutti i tag che potrebbero contenere i titoli delle tesi
            for elemento in soup.find_all(['h3', 'h4', 'p', 'span', 'li', 'strong', 'a']):
                testo = elemento.get_text().strip()
                testo_low = testo.lower()
                
                # FILTRO INTELLIGENTE:
                # Cerchiamo parole che appaiono tipicamente nelle proposte di tesi
                parole_chiave = ["topic", "thesis", "abstract", "tesi", "proposta", "titolo", "supervisor"]
                
                if len(testo) > 15: # Evitiamo scritte troppo corte come i nomi dei menù
                    if any(p in testo_low for p in parole_chiave):
                        if testo not in tesi_attuali:
                            tesi_attuali.append(testo)
                            print(f"Trovata possibile tesi: {testo[:50]}...")

            # --- GESTIONE STORICO ---
            file_storico = "tesi_viste.txt"
            if os.path.exists(file_storico):
                with open(file_storico, "r", encoding="utf-8") as f:
                    viste = f.read().splitlines()
            else:
                viste = []

            # Identifica solo quelle che non abbiamo mai visto
            nuove = [t for t in tesi_attuali if t not in viste]

            if nuove:
                messaggio = "🎓 *Nuove Tesi RFX trovate!*\n\n"
                for n in nuove:
                    messaggio += f"• {n}\n\n"
                
                invia_telegram(messaggio)
                
                # Salva nello storico
                with open(file_storico, "a", encoding="utf-8") as f:
                    for n in nuove:
                        f.write(n + "\n")
            else:
                print("Nessuna nuova tesi rilevata rispetto all'ultimo controllo.")
        else:
            print(f"Il sito/proxy ha risposto con errore: {response.status_code}")

    except Exception as e:
        print(f"Errore durante lo scraping: {e}")

if __name__ == "__main__":
    controlla()
