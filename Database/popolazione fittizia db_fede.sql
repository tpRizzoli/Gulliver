use Gulliver;

INSERT INTO utenti (username, email, pwd) VALUES
('alice', 'alice@example.com', 'password123'),
('bob', 'bob@example.com', 'securepwd'),
('charlie', 'charlie@example.com', 'password');

INSERT INTO itinerari (nome, sysDefault) VALUES 
('Esplorando le Alpi', 1),
('Spiagge e Relax', 1),
('Tesori del Sud', 1),
('Camminando per la Costa Amalfitana', 1);

INSERT INTO tipologie (nome) VALUES
('Escursionismo'), 
('Nuoto'),
('Visita musei'),
('Cucina'),
('Ciclismo'),
('Scalata'),
('Relax');

-- Inserimento delle attività
INSERT INTO attivita (nome, difficolta, id_tipologia, descrizione) 
VALUES 
('Escursione sul Monte Bianco', 4, 1, 'Escursione impegnativa sulla vetta più alta delle Alpi'),
('Trekking nei Pirenei', 3, 1, 'Lungo cammino tra i paesaggi montani dei Pirenei'),
('Escursionismo in montagna', 3, 1, 'Escursioni a piedi o in bicicletta per ammirare la bellezza naturale delle montagne italiane'),

('Nuotata al mare', 2, 2, 'Nuotata rilassante nelle acque cristalline del Mediterraneo'),
('Lezione di nuoto sincronizzato', 3, 2, 'Allenamento di nuoto sincronizzato in piscina'),
('Tour in barca', 1, 2, 'Un tour in barca per ammirare le coste e le isole tipiche della costiera amalfitana'),

('Visita al Louvre', 1, 3, 'Esplorazione delle opere d arte presso il famoso museo parigino'),
('Tour guidato del British Museum', 2, 3, 'Visita guidata delle collezioni storiche del British Museum'),
('Tour al museo della scienza della tecnica', 1, 3, 'Visita guidata Museo Nazionale della Sciena e della Tecnica');

INSERT INTO attivita_itinerari (id_attivita, id_itinerario) VALUES
(15, 1), 
(16, 1),
(17, 1), 

(18, 2),
(19, 2),
(20, 2),

(21, 3),
(22, 3),
(23, 3);

INSERT INTO attivita_luoghi (id_attivita, id_luogo) VALUES
(15, 1),
(16, 2),
(17, 3),

(18, 9),
(19, 4),
(20, 5),

(21, 6),
(22, 6),
(23, 6);

INSERT INTO luoghi_categorie (id_luogo, id_categoria) VALUES
-- 1 mare 2 montagna 3 citta
(3, 1),
(6, 1),
(8, 1),

(1, 2),
(2, 2),
(10, 2),

(3, 3),
(5, 3),
(11, 3);
