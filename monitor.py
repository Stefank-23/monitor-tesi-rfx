import requests
from bs4 import BeautifulSoup
import os

# Configurazioni (prese dai "Secrets" di GitHub)
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = "https://www.igi.cnr.it/formazione/tesi-laurea/" # Verifica l'URL esatto

def invia_telegram(messaggio):
    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": messaggio, "parse_mode": "Markdown"}
    requests.post(url_tg, data=payload)

def controlla():
    try:
        response = requests.get(URL, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Cerchiamo i link alle tesi (di solito sono dentro tag <a>)
        # Questo punto potrebbe richiedere un piccolo aggiustamento in base al sito
        tesi_attuali = []
        for link in soup.find_all('a'):
            testo = link.get_text().strip()
            # Filtriamo solo i link che sembrano titoli di tesi
            if len(testo) > 10 and ("Tesi" in testo or "Project" in testo or "Abstract" in testo or "Topic of thesis" in testo):
                tesi_attuali.append(testo)

        # Leggi tesi già viste
        if os.path.exists("tesi_viste.txt"):
            with open("tesi_viste.txt", "r", encoding="utf-8") as f:
                viste = f.read().splitlines()
        else:
            viste = []

        nuove = [t for t in tesi_attuali if t not in viste]

        if nuove:
            messaggio = "🔔 **Nuove Tesi Disponibili!**\n\n" + "\n".join([f"- {n}" for n in nuove])
            invia_telegram(messaggio)
            
            # Aggiorna il file
            with open("tesi_viste.txt", "a", encoding="utf-8") as f:
                for n in nuove:
                    f.write(n + "\n")
            return True
    except Exception as e:
        print(f"Errore: {e}")
    return False

if __name__ == "__main__":
    controlla()
          git config --global user.email 'action@github.com'
          git add tesi_viste.txt
          git commit -m "Aggiornato registro tesi" || exit 0
          git push
