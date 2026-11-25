-- Attivazione controllo chiavi esterne FK
PRAGMA FOREIGN_key = on;

-- CREAZIONE DEL DATABASE

-- SI RENDE LO SCRIPT ESEGUIBILE PIU VOLTE

DROP TABLE if EXISTS spesa;
DROP TABLE if EXISTS budget;
DROP TABLE if EXISTS categoria;

-- CREAZIONE DELLE TABELLE
-- categoria
CREATE TABLE categoria (
	id_categoria	INTEGER PRIMARY KEY AUTOINCREMENT,
	nome			TEXT NOT NULL
					UNIQUE
					CHECK (length(trim(nome)) >0)
);
-- spesa
CREATE TABLE spesa (
	id_spesa		INTEGER PRIMARY KEY AUTOINCREMENT,
	data 			TEXT NOT NULL 				-- formato yyyy-mm-dd
					CHECK(length(data)=10),		
	importo			REAL NOT NULL
					CHECK (importo >0),
	descrizione 	TEXT,
	id_categoria	INTEGER NOT NULL,
	FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria)
);
-- budget
CREATE TABLE budget (
	id_budget		INTEGER PRIMARY KEY AUTOINCREMENT,
	mese			TEXT NOT NULL 				-- formato yyyy-dd
					CHECK (length(mese)=7),
	importo			REAL NOT null 
					CHECK (importo >0),
	id_categoria	INTEGER NOT NULL,
	FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria),
	UNIQUE (mese, id_categoria)
);

-- inserimento categorie



-- TEST DEI VINCOLI IMPOSTI

-- check importo negativo
--INSERT INTO spesa (data, importo, descrizione, id_categoria) VALUES ('2025-03-01', -5,'ERRORE', 	1);

-- check FK
--INSERT INTO spesa (data, importo, descrizione, id_categoria) VALUES ('2025-03-01', 10, 'ERRORE', 	99);

-- check unique su Cibo
--INSERT INTO categoria (nome) VALUES ('Cibo');

-- CHECK unique su Budget
--INSERT INTO budget (mese, importo, id_categoria) VALUES ('2025-01', 500, 	1);

--check not null su Data 
-- INSERT into spesa (data, importo, descrizione, id_categoria) VALUES ( NULL, 10,'ERRORE', 	1);

--check nome categoria vuoto
--INSERT INTO categoria (nome) VALUES ('   ');


-- tutte le query sono sotto commento in modo da poterle avviare singolarmente su richiesta
