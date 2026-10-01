from csv import writer
from operator import itemgetter

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""

    try:
        with open(file_path, 'r') as elenco_foto:
            album_fotografico={}
            intestazione=elenco_foto.readline()

            for riga in  elenco_foto:
                (codice, titolo, autore, mese, anno) = riga.strip().split(',')

                mese=int(mese)
                anno=int(anno)

                if anno not in album_fotografico:
                    album_fotografico[anno] = [[codice,titolo,autore,mese]]
                else:
                    album_fotografico[anno].append([codice,titolo,autore,mese])

            for anno, foto in album_fotografico.items():
                print(f'{anno}:')
                for elemento in foto:
                    print(f'{elemento[0]}, {elemento[1]}, {elemento[2]}, {elemento[3]}')
                print()
            return album_fotografico
    except FileNotFoundError:
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    if mese < 1 or mese > 12:
        return None

    for anno_album in album:
        for elemento in album[anno_album]:
            if elemento[0]==codice:
                return None

    try:
        with open(file_path, 'a') as elenco_foto:
            csvWriter = writer(elenco_foto)
            csvWriter.writerow([codice, titolo, autore, mese, anno])
    except FileNotFoundError:
        return None

    nuova_foto = [codice, titolo, autore, mese]

    if anno not in album:
        album[anno]=[nuova_foto]
    else:
        album[anno].append(nuova_foto)

    return nuova_foto


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""

    for anno_album in album:
        for elemento in album[anno_album]:
            if codice == elemento[0]:
                return f'{elemento[0]}, {elemento[1]}, {elemento[2]}, {elemento[3]}, {anno_album}'

    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""

    for anno_album in album:
        if anno==anno_album:
            foto_ordinate=sorted(album[anno_album], key=itemgetter(1))  #ordina secondo il titolo che si trova in posizione 1 dentro ogni lista
            return [elemento[1] for elemento in foto_ordinate]
    return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
