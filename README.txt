# Sistema di gestione delle spese personali con definizione di budget

realizzato in PYTHON con database relazione SQLITE

OPERAZIONI POSSIBILI:
	- registrare spese giornaliere
	- organizzarle per categoria
	- definire budget mensili per ogni categoria
	- visualizzare report riepilogativi e confrontarli con i budget scelti




REQUISITI

- INTERPRETE : PYTHON VERSIONE ALMENO 3.10 O SUPERIORE [ il programma include match/case]
- LIBRERIE : STANDARD DI PYTHON [sqlite3, math, datetime, pathlib]
- DATABASE : SQLITE incluso con python




Per controllare se la versione di python é corretta da terminale :
	python --version





ESECUZIONE DEL PROGRAMMA

1.	Scaricare il programma e aprire il terminale nella cartella principale del progetto tramite
		python src\main.py



Al primo avvio il programma crea il file spese.db eseguendo lo script 'sql/database.sql'. 
Nei successivi avvii il programma usa il database giá creato e mantiene salvati i dati inseriti

Per resettare tutto basta cancellare il file spese.db





STRUTTURA DEL REPOSITORY
	PersonalExpenseSystem
	|--- src/
	|	|--- main.py
	|--- sql/
	|	|--- database.sql
	|---demo/
	|	|--- demo_video.mp4
	|---README.md









FUNZIONALITA 

All'avvio si presenta il menu principale di scelta con :
	1. GESTIONE CATEGORIE		/ permette di inserire le nuove categorie, non accetta campo vuoto oppure nome gia usaato
	2. INSERISCI SPESA		/ permette di inserire una spesa con data, importo categoria e descrizione se si vuole, non accetta importo minore di 0 e categoria vuota 
	3. DEFINISCI BUDGET		/ permette di definire un budget per una categoria in un mese scelto. SE il budget in un mese é gia definito verra aggiornato
	4. VISUALIZZA REPORT		/ apre un sottomenu per i tre report disponibili
	5. ESCI				/ chiude il programma



REPORT DISPONIBILI
	
	1. TOTALE SPESE PER CATEGORIA		/ elenco delle spese di una categoria
	2. SPESE MENSILI VS BUDGET		/ confronta le spese effettuate con il budget scelto
	3. ELENCO COMPLETO DELLE SPESE		/ stipula un elenco totale delle spese in ordine di data



VINCOLI DI INSERIMENTO DATI


--- DATA --- deve essere in formato YYYY-MM-DD altrimenti il programma crea errore

--- MESE --- deve essere in formato YYYY-MM altrimenti il programma crea errore

--- IMPORTO --- maggiore di zero




DATABASE
	
TABELLA CATEGORIA ---- id_categoria, nome, | 
	VINCOLI ---- PRIMARY KEY, NOT NULL, UNIQUE, CHECK


TABELLA SPESA ---- id_spesa, data, importo, descrizione, id_categoria
	VINCOLI ---- PRIMARY KEY, FOREIGN KEY, NOT NULL, CHECK(importo > 0)


TABELLA BUDGET ---- id_budget, mese, importo, id_categoria
	VINCOLI ---- PRIMARY KEY, FOREIGN KEY, NOT NULL, CHECK(importo > 0), UNIQUE(mese, categoria)



RELAZIONE 1 a N ----> una categoria puo avere molte spese e budget

Aprendo il file database.sql é possibile visionare lo script completo



DEMO


Video demo che dimostra il funzionamento del programma 

















