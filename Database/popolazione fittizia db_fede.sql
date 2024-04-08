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
(1, 1), 
(2, 1),
(3, 1), 

(4, 2),
(5, 2),
(6, 2),

(7, 3),
(8, 3),
(9, 3);

INSERT INTO luoghi (nome, stato, longitudine, latitudine) 
VALUES
('Monte Bianco', 'Italia', 45.8325, 6.8650), -- Luogo di montagna
('Pirenei', 'Francia', 42.6611, 0.3328), -- Luogo di montagna
('Mediterraneo', 'Mare', 35.0000, 18.0000), -- Luogo di mare
('Parigi', 'Francia', 48.8566, 2.3522), -- Luogo di città
('Londra', 'Regno Unito', 51.5074, -0.1278), -- Luogo di città
('Tanzania', 'Tanzania', -6.3690, 34.8888), -- Luogo di mare
('Maldive', 'Maldive', 3.2028, 73.2207), -- Luogo di mare
('Yosemite National Park', 'Stati Uniti', 37.8651, -119.5383), -- Luogo di montagna
('Roma', 'Italia', 41.8933203, 12.4829321); -- Luogo di città


INSERT INTO attivita_luoghi (id_attivita, id_luogo) VALUES
(1, 1),
(2, 2),
(3, 3),

(4, 9),
(5, 4),
(6, 5),

(7, 6),
(8, 6),
(9, 6);


-- FIXARE QUESTO:

INSERT INTO luoghi_categorie (id_luogo, id_categoria) VALUES
-- 1 mare 2 montagna 3 citta
(1, 2),
(2, 2),
(6, 2),

(4, 3),
(5, 3),
(9, 3),


(7, 1),
(3, 1),
(8, 1);
