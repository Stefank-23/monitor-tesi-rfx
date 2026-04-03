import requests
from bs4 import BeautifulSoup
import os

# Recupera le chiavi segrete dai Secrets di GitHub
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# URL della pagina del Consorzio RFX (Verifica che sia corretto)
URL = "https://www.igi.cn/formazione/tesi-di-laurea-magistrale/"

def invia_telegram(messaggio):
    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": messaggio, "parse_mode": "Markdown"}
    try:
        requests.post(url_tg, data=payload)
    except Exception as e:
        print(f"Errore invio Telegram: {e}")

def controlla():
    try:
        response = requests.get(URL, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tesi_attuali = []
        # Cerchiamo tutti i link e i testi nella pagina
        for elemento in soup.find_all(['a', 'h3', 'p']):
            testo = elemento.get_text().strip()
            
            # Applichiamo i tuoi filtri
            if len(testo) > 10:
                if "Topic of thesis" in testo or "Abstract" in testo:
                    if testo not in tesi_attuali:
                        tesi_attuali.append(testo)

        # Gestione del file storico
        file_storico = "tesi_viste.txt"
        if os.path.exists(file_storico):
            with open(file_storico, "r", encoding="utf-8") as f:
                viste = f.read().splitlines()
        else:
            viste = []

        # Trova le novità
        nuove = [t for t in tesi_attuali if t not in viste]

        if nuove:
            messaggio = "🔔 *Nuove Tesi RFX trovate!*\n\n" + "\n".join([f"• {n}" for n in nuove])
            invia_telegram(messaggio)
            
            # Aggiorna il file locale
            with open(file_storico, "a", encoding="utf-8") as f:
                for n in nuove:
                    f.write(n + "\n")
            print(f"Trovate {len(nuove)} novità.")
        else:
            print("Nessuna nuova tesi trovata.")
            
    except Exception as e:
        print(f"Errore durante lo scraping: {e}")

if __name__ == "__main__":
    controlla()
