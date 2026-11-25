-- ============================================================
-- A) CREAZIONE DEL DATABASE
-- ============================================================

-- Attivazione controllo chiavi esterne FK
PRAGMA foreign_keys = ON;

-- Si rende lo script eseguibile piu volte
DROP TABLE IF EXISTS spesa;
DROP TABLE IF EXISTS budget;
DROP TABLE IF EXISTS categoria;

-- CREAZIONE DELLE TABELLE

-- categoria
CREATE TABLE categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL
                 UNIQUE
                 CHECK (length(trim(nome)) > 0)
);

-- spesa
CREATE TABLE spesa (
    id_spesa     INTEGER PRIMARY KEY AUTOINCREMENT,
    data         TEXT NOT NULL            -- formato yyyy-mm-dd
                 CHECK (length(data) = 10),
    importo      REAL NOT NULL
                 CHECK (importo > 0),
    descrizione  TEXT,
    id_categoria INTEGER NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria)
);

-- budget
CREATE TABLE budget (
    id_budget    INTEGER PRIMARY KEY AUTOINCREMENT,
    mese         TEXT NOT NULL            -- formato yyyy-mm
                 CHECK (length(mese) = 7),
    importo      REAL NOT NULL
                 CHECK (importo > 0),
    id_categoria INTEGER NOT NULL,
    FOREIGN KEY (id_categoria) REFERENCES categoria (id_categoria),
    UNIQUE (mese, id_categoria)
);

-- ============================================================
-- B) INSERIMENTO DEI DATI DI ESEMPIO
-- ============================================================

-- categorie (gli id 1, 2, 3, 4 vengono assegnati in ordine)
INSERT INTO categoria (nome) VALUES
    ('Alimentari'),
    ('Trasporti'),
    ('Svago'),
    ('Casa');

-- spese di gennaio 2025
INSERT INTO spesa (data, importo, descrizione, id_categoria) VALUES
    ('2025-01-15',  25.00, 'Pranzo',             1),
    ('2025-01-05',  95.00, 'Spesa settimanale',  1),
    ('2025-01-12', 110.00, 'Spesa supermercato', 1),
    ('2025-01-26',  90.00, 'Cena di famiglia',   1),
    ('2025-01-03',  40.00, 'Abbonamento bus',    2),
    ('2025-01-14',  35.00, 'Benzina',            2),
    ('2025-01-28',  45.00, 'Benzina',            2),
    ('2025-01-18',  30.00, 'Cinema',             3),
    ('2025-01-22',  30.00, 'Libro',              3),
    ('2025-01-10',  70.00, 'Bolletta luce',      4);

-- spese di febbraio 2025
INSERT INTO spesa (data, importo, descrizione, id_categoria) VALUES
    ('2025-02-02',  80.00, 'Spesa settimanale',  1),
    ('2025-02-09',  45.50, 'Spesa supermercato', 1),
    ('2025-02-04',  50.00, 'Abbonamento bus',    2);

-- budget mensili
INSERT INTO budget (mese, importo, id_categoria) VALUES
    ('2025-01', 300.00, 1),
    ('2025-01', 150.00, 2),
    ('2025-01',  80.00, 3),
    ('2025-02', 350.00, 1),
    ('2025-02',  40.00, 2);

-- ============================================================
-- C) DIMOSTRAZIONE DEI VINCOLI DI INTEGRITA'
-- Tutte le istruzioni di prova sono sotto commento: per
-- provarne una, togliere i "--" dalle sue righe. Ognuna
-- deve dare un errore, perche viola un vincolo.
-- ============================================================

-- CHECK: importo negativo
-- INSERT INTO spesa (data, importo, descrizione, id_categoria)
--     VALUES ('2025-03-01', -5, 'ERRORE', 1);

-- FOREIGN KEY: la categoria 99 non esiste
-- INSERT INTO spesa (data, importo, descrizione, id_categoria)
--     VALUES ('2025-03-01', 10, 'ERRORE', 99);

-- UNIQUE: la categoria Alimentari esiste gia
-- INSERT INTO categoria (nome) VALUES ('Alimentari');

-- UNIQUE: esiste gia un budget per Alimentari a gennaio 2025
-- INSERT INTO budget (mese, importo, id_categoria)
--     VALUES ('2025-01', 500, 1);

-- NOT NULL: manca la data
-- INSERT INTO spesa (data, importo, descrizione, id_categoria)
--     VALUES (NULL, 10, 'ERRORE', 1);

-- CHECK: nome categoria vuoto
-- INSERT INTO categoria (nome) VALUES ('   ');
