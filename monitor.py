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
4. Imposta l'automazione (GitHub Actions)
Ora dobbiamo dire a GitHub di premere "Play" per noi ogni giorno.

Nel tuo repository, vai nella scheda Actions.

Clicca su "set up a workflow yourself".

Incolla questo codice (che farà girare lo script ogni giorno alle 8:00 e alle 18:00):

YAML
name: Monitor Tesi RFX
on:
  schedule:
    - cron: '0 8,18 * * *' # Gira due volte al giorno
  workflow_dispatch: # Permette di avviarlo a mano per test

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout codice
        uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Installa dipendenze
        run: pip install -r requirements.txt
      - name: Esegui script
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python monitor.py
      - name: Salva modifiche
        run: |
          git config --global user.name 'GitHub Action'
          git config --global user.email 'action@github.com'
          git add tesi_viste.txt
          git commit -m "Aggiornato registro tesi" || exit 0
          git push
