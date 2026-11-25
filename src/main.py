import sqlite3
import math
from pathlib import Path
from datetime import datetime

CARTELLA_PROGETTO = Path(__file__).resolve().parent.parent
FILE_DATABASE = CARTELLA_PROGETTO / "spese.db"
FILE_SQL = CARTELLA_PROGETTO / "sql" / "database.sql"


def apri_database():
    conn = sqlite3.connect(FILE_DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()
    cursor.execute("select name from sqlite_master where type='table' and name='categoria';")
    if cursor.fetchone() is None:
        with open(FILE_SQL, "r", encoding="utf-8") as file:
            conn.executescript(file.read())
        print("Database creato con i dati di esempio.")
    return conn
### fino qui si crea il database se non esiste, altrimenti lo apre e lo restituisce.


# funzioni di validazione e verifica degli input

def cerca_categoria(conn, nome):                      # ricerca di una categoria
    cursor = conn.execute("SELECT id_categoria FROM categoria WHERE nome = ? COLLATE NOCASE", (nome,))
    riga = cursor.fetchone()
    if riga is None:
        return None
    return riga[0]


def num_importo(testo):                               # trasforma il testo in valore numerico
    try:
        valore = float(testo.replace(",", "."))
    except ValueError:
        return None
    if not math.isfinite(valore):
        return None
    return round(valore, 2)


def formato_data(testo):                              # gestione del formato di "Data"
    if len(testo) != 10:
        return False
    try:
        datetime.strptime(testo, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def formato_mese(testo):                              # gestione del formato di "Mese"
    if len(testo) != 7:
        return False
    try:
        datetime.strptime(testo, "%Y-%m")
        return True
    except ValueError:
        return False


# MODULI

# Menu 1 : Gestione categoria
def gestione_categorie(conn):
    print()
    print("---- Gestione Categorie ----")
    nome = input("Nome della categoria: ").strip()

    if nome == "":
        print("Errore: il nome della categoria non può essere vuoto.")
        return

    if cerca_categoria(conn, nome) is not None:
        print("La categoria esiste già.")
        return

    conn.execute("INSERT INTO categoria (nome) VALUES (?)", (nome,))
    conn.commit()
    print("Categoria inserita correttamente.")


# Menu 2 : Inserimento spesa
def inserisci_spesa(conn):
    print()
    print("---- Inserisci una Spesa ----")

    data = input("Data (formato YYYY-MM-DD): ").strip()
    testo_importo = input("Importo: ").strip()
    nome_categoria = input("Nome della categoria: ").strip()
    descrizione = input("Descrizione (facoltativa): ").strip()

    if not formato_data(data):
        print("Errore: la data non è valida. Usa il formato YYYY-MM-DD.")
        return

    importo = num_importo(testo_importo)
    if importo is None:
        print("Errore: l'importo non è un numero valido.")
        return
    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return

    id_categoria = cerca_categoria(conn, nome_categoria)
    if id_categoria is None:
        print("Errore: la categoria non esiste.")
        return

    if descrizione == "":
        descrizione = None

    conn.execute("INSERT INTO spesa (data, importo, descrizione, id_categoria) VALUES (?, ?, ?, ?)", (data, importo, descrizione, id_categoria))
    conn.commit()
    print("Spesa inserita correttamente.")


# Menu 3 : Definizione del budget mensile
def definisci_budget(conn):
    print()
    print("---- Definisci Budget Mensile ----")

    mese = input("Mese (formato YYYY-MM): ").strip()
    nome_categoria = input("Nome della categoria: ").strip()
    testo_importo = input("Importo del budget: ").strip()

    if not formato_mese(mese):
        print("Errore: il mese non è valido. Usa il formato YYYY-MM.")
        return

    importo = num_importo(testo_importo)
    if importo is None:
        print("Errore: il budget non è un numero valido.")
        return
    if importo <= 0:
        print("Errore: il budget deve essere maggiore di zero.")
        return

    id_categoria = cerca_categoria(conn, nome_categoria)
    if id_categoria is None:
        print("Errore: la categoria non esiste.")
        return

    cursor = conn.execute("SELECT id_budget FROM budget WHERE mese = ? AND id_categoria = ?", (mese, id_categoria))
    if cursor.fetchone() is None:
        conn.execute("INSERT INTO budget (mese, importo, id_categoria) VALUES (?, ?, ?)", (mese, importo, id_categoria))
    else:
        conn.execute("UPDATE budget SET importo = ? WHERE mese = ? AND id_categoria = ?", (importo, mese, id_categoria))

    conn.commit()
    print("Budget mensile salvato correttamente.")


# Menu 4 : Report

# Report 1
def report_totale_categoria(conn):
    print()
    print("---- Totale Spese per Categoria ----")

    cursor = conn.execute("""
        SELECT categoria.nome, SUM(spesa.importo)
        FROM spesa
        JOIN categoria ON spesa.id_categoria = categoria.id_categoria
        GROUP BY categoria.id_categoria
        ORDER BY categoria.nome
    """)
    righe = cursor.fetchall()

    if len(righe) == 0:
        print("Nessuna spesa registrata.")
        return

    print("Categoria".ljust(20, ".") + "Totale Speso")
    for nome, totale in righe:
        print(nome.ljust(20, ".") + f"{totale:.2f}")


# Report 2
def report_spese_budget(conn):
    print()
    print("---- Spese mensili vs Budget ----")

    cursor = conn.execute("""
        SELECT budget.mese, categoria.nome, budget.importo,
               round(COALESCE(SUM(spesa.importo), 0), 2) AS speso
        FROM budget
        JOIN categoria ON budget.id_categoria = categoria.id_categoria
        LEFT JOIN spesa ON spesa.id_categoria = budget.id_categoria
                       AND substr(spesa.data, 1, 7) = budget.mese
        GROUP BY budget.id_budget, budget.mese, categoria.nome, budget.importo
        ORDER BY budget.mese, categoria.nome
    """)
    righe = cursor.fetchall()

    if len(righe) == 0:
        print("Nessun budget definito.")
        return

    for mese, nome, budget, speso in righe:
        if speso > budget:
            stato = "SUPERAMENTO BUDGET"
        else:
            stato = "NEL BUDGET"

        print()
        print("Mese:", mese)
        print("Categoria:", nome)
        print(f"Budget: {budget:.2f}")
        print(f"Speso: {speso:.2f}")
        print("Stato:", stato)


# Report 3
def report_elenco_spese(conn):
    print()
    print("---- Elenco completo delle Spese ----")

    cursor = conn.execute("""
        SELECT spesa.data, categoria.nome, spesa.importo, spesa.descrizione
        FROM spesa
        JOIN categoria ON spesa.id_categoria = categoria.id_categoria
        ORDER BY spesa.data, spesa.id_spesa
    """)
    righe = cursor.fetchall()

    if len(righe) == 0:
        print("Nessuna spesa registrata.")
        return

    print(f"{'Data':<12}{'Categoria':<16}{'Importo':>9}  Descrizione")
    print("-" * 62)
    for data, nome, importo, descrizione in righe:
        if descrizione is None:
            descrizione = ""
        print(f"{data:<12}{nome:<16}{importo:>9.2f}  {descrizione}")


# Sottomenu dei report
def visualizza_report(conn):
    while True:
        print()
        print("-------------------------")
        print("REPORT")
        print("-------------------------")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        print("-------------------------")
        scelta = input("Inserisci la tua scelta: ").strip()

        match scelta:
            case "1":
                report_totale_categoria(conn)
            case "2":
                report_spese_budget(conn)
            case "3":
                report_elenco_spese(conn)
            case "4":
                return
            case _:
                print("Scelta non valida. Riprovare.")


# Funzione Menu
def mostra_menu():
    print()
    print("-------------------------")
    print("SISTEMA SPESE PERSONALI")
    print("-------------------------")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("-------------------------")


def main():
    conn = apri_database()
    print("Benvenuto nel Sistema di Gestione delle Spese Personali!")

    # ciclo per il menu
    while True:
        mostra_menu()
        scelta = input("Inserisci la tua scelta: ").strip()

        match scelta:
            case "1":
                gestione_categorie(conn)
            case "2":
                inserisci_spesa(conn)
            case "3":
                definisci_budget(conn)
            case "4":
                visualizza_report(conn)
            case "5":
                print("Chiusura...")
                break
            case _:
                print("Scelta non valida. Riprovare.")

    conn.close()


if __name__ == "__main__":
    main()
