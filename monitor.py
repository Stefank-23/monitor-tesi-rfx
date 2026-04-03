def controlla():
    url_test = "https://it.wikipedia.org/wiki/Energia_nucleare"
    tesi_attuali = []
    
    try:
        print(f"Test di funzionamento su: {url_test}")
        response = requests.get(url_test, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cerchiamo i titoli dei paragrafi
            for elemento in soup.find_all(['h2', 'h3']):
                testo = elemento.get_text().strip()
                testo_low = testo.lower()
                
                # Filtro di prova
                if len(testo) > 5:
                    if "nucleare" in testo_low or "reattore" in testo_low:
                        if testo not in tesi_attuali:
                            tesi_attuali.append(testo)
                            print(f"DEBUG - Trovato: {testo}")

            # Caricamento storico
            file_storico = "tesi_viste.txt"
            if os.path.exists(file_storico):
                with open(file_storico, "r", encoding="utf-8") as f:
                    viste = f.read().splitlines()
            else:
                viste = []

            nuove = [t for t in tesi_attuali if t not in viste]

            if nuove:
                messaggio = "🧪 *Test Wikipedia Funzionante!*\n\n" + "\n".join([f"• {n}" for n in nuove])
                invia_telegram(messaggio)
                with open(file_storico, "a", encoding="utf-8") as f:
                    for n in nuove:
                        f.write(n + "\n")
            else:
                print("Nessuna novità (o titoli già salvati in precedenza).")
        else:
            print(f"Errore risposta sito: {response.status_code}")
            
    except Exception as e:
        print(f"Errore durante lo scraping: {e}")            # Gestione storico e notifiche
            file_storico = "tesi_viste.txt"
            if os.path.exists(file_storico):
                with open(file_storico, "r", encoding="utf-8") as f:
                    viste = f.read().splitlines()
            else:
                viste = []

            nuove = [t for t in tesi_attuali if t not in viste]

            if nuove:
                messaggio = "🔔 *Nuove Tesi RFX!*\n\n" + "\n".join([f"• {n}" for n in nuove])
                invia_telegram(messaggio)
                with open(file_storico, "a", encoding="utf-8") as f:
                    for n in nuove: f.write(n + "\n")
            else:
                print("Connessione riuscita, ma nessuna tesi trovata con quei filtri.")
        else:
            print(f"Il proxy ha risposto con errore: {response.status_code}")

    except Exception as e:
        print(f"Errore durante lo scraping: {e}")
