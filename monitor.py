def controlla():
    # URL originale "impacchettato" nel proxy per evitare il timeout
    url_base = "https://www.igi.cn/formazione/tesi-di-laurea-magistrale/"
    proxy_url = f"https://api.allorigins.win/raw?url={url_base}"
    
    tesi_attuali = []
    
    try:
        print(f"Tentativo di connessione tramite proxy a: {url_base}")
        # Chiamata tramite il servizio AllOrigins
        response = requests.get(proxy_url, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cerchiamo in tutti i tag possibili
            for elemento in soup.find_all(['a', 'h3', 'h4', 'p', 'span', 'li', 'div']):
                testo = elemento.get_text().strip()
                testo_low = testo.lower()
                
                if len(testo) > 5:
                    print(f"DEBUG - Vedo questo: {testo}")
                    # Per ora commentiamo il filtro delle parole chiave
                    # if any(p in testo_low for p in parole):
                    tesi_attuali.append(testo)
                    
                # Filtri per parole chiave
               # if len(testo) > 10:
                #    parole = ["topic", "thesis", "abstract", "tesi", "proposta"]
                 #   if any(p in testo_low for p in parole):
                  #      if testo not in tesi_attuali:
                   #         tesi_attuali.append(testo)
                    #        print(f"DEBUG - Trovato: {testo}")

            # Gestione storico e notifiche
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
