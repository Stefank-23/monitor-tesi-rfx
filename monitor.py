def controlla():
    # Usiamo Wikipedia come test: è stabile e non blocca gli script
    url_test = "https://it.wikipedia.org/wiki/Energia_nucleare"
    
    tesi_attuali = []
    
    try:
        print(f"Test di funzionamento su: {url_test}")
        # Su Wikipedia non serve il proxy, basta una richiesta normale
        response = requests.get(url_test, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Cerchiamo i titoli dei paragrafi (tag h2 e h3)
            for elemento in soup.find_all(['h2', 'h3']):
                testo = elemento.get_text().strip()
                
                # Usiamo una parola chiave che sappiamo esistere su Wikipedia
                if len(testo) > 5:
                    # Se il titolo contiene "nucleare" o "reattore", lo prendiamo
                    testo_low = testo.lower()
                    if "nucleare" in testo_low or "reattore" in testo_low:
                        tesi_attuali.append(testo)
                        print(f"DEBUG - Trovato: {testo}")}")

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
