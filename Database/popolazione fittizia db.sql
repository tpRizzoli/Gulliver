use Gulliver;

-- Inserimento degli utenti
INSERT INTO utenti (username, email, pwd) VALUES
('alice', 'alice@example.com', 'password123'),
('bob', 'bob@example.com', 'securepwd'),
('charlie', 'charlie@example.com', 'password'),
('daniel', 'daniel@example.com', 'daniel123'),
('emma', 'emma@example.com', 'emma456'),
('frank', 'frank@example.com', 'frank789'),
('grace', 'grace@example.com', 'gracepwd'),
('harry', 'harry@example.com', 'harry123'),
('isabella', 'isabella@example.com', 'isabella456');

-- Inserimento degli itinerari
INSERT INTO itinerari (nome, sysDefault) VALUES 
('Esplorando le Alpi', 1),
('Città d\'Arte Italiane', 0),
('Spiagge e Relax', 1),
('Scoprendo la Toscana', 1),
('Tesori del Sud', 0),
('Camminando per la Costa Amalfitana', 0),
('Viaggio tra i Borghi Medievali', 0),
('Tour Enogastronomico nel Piemonte', 0),
('Navigando tra le Isole Greche', 0);

-- Inserimento delle tipologie di attività
INSERT INTO tipologie (nome) VALUES
('Escursionismo'),
('Nuoto'),
('Visita musei'),
('Cucina'),
('Safari'),
('Snorkeling'),
('Ciclismo'),
('Scalata'),
('Camping'),
('Visita monumenti'),
('Scherma'),
('Relax'),
('Visita teatri'),
('Tour');

-- Inserimento delle attività
INSERT INTO attivita (nome, difficolta, id_tipologia, descrizione) 
VALUES 
('Escursione sul Monte Bianco', 4, 1, 'Escursione impegnativa sulla vetta più alta delle Alpi'),
('Trekking nei Pirenei', 3, 1, 'Lungo cammino tra i paesaggi montani dei Pirenei'),
('Nuotata al mare', 2, 2, 'Nuotata rilassante nelle acque cristalline del Mediterraneo'),
('Lezione di nuoto sincronizzato', 3, 2, 'Allenamento di nuoto sincronizzato in piscina'),
('Visita al Louvre', 1, 3, 'Esplorazione delle opere d\'arte presso il famoso museo parigino'),
('Tour guidato del British Museum', 2, 3, 'Visita guidata delle collezioni storiche del British Museum'),
('Corso di cucina italiana', 3, 4, 'Lezioni pratiche per imparare a cucinare autentici piatti italiani'),
('Corso di pasticceria francese', 4, 4, 'Impara a creare deliziosi dolci francesi come un vero chef'),
('Safari in Tanzania', 5, 5, 'Esplorazione della savana africana alla ricerca di animali selvatici'),
('Safari fotografico in Kenya', 4, 5, 'Caccia fotografica ai magnifici animali della savana'),
('Snorkeling alle Maldive', 2, 6, 'Esperienza subacquea per ammirare i meravigliosi coralli e la fauna marina'),
('Escursione in barca a vela', 3, 6, 'Esplorazione delle acque tropicali in barca a vela'),
('Ciclismo in montagna', 3, 7, 'Percorso in bicicletta attraverso i panorami mozzafiato delle Alpi'),
('Tour in bicicletta delle cantine', 2, 7, 'Passeggiata in bicicletta tra le cantine e i vigneti del sud della Francia'),
('Scalata su roccia', 4, 8, 'Affronta le sfide verticali della scalata su roccia in un ambiente naturale'),
('Lezione di arrampicata indoor', 2, 8, 'Allenamento e pratica di arrampicata in palestra specializzata'),
('Camping nel Parco Nazionale Yosemite', 3, 9, 'Avventura nel cuore della natura con tenda e fuoco campeggio'),
('Escursione notturna con il fuoco', 2, 9, 'Camminata notturna sotto le stelle con accampamento e falò'),
('Visita del Colosseo', 1, 10, 'Esplora le aree sotterranee e scopri la storia di Roma.'),
('Lezione di scherma gladiatoria', 3, 11, 'Impara a maneggiare le armi utilizzate dai gladiatori nellantica Roma.'),
('Lezione di pasta fatta in casa', 2, 4, 'Impara a fare la pasta perfetta da chef locali.'),
('Ciclismo in Toscana', 3, 7, 'Scopri la campagna toscana e le piccole comunità che si trovano tra i borghi medievali.'),
('Visita alle terme', 1, 12, 'Bagno termale nelle acque termali naturali, per rilassarsi e rigenerarsi.'),
('Tour in barca', 1, 2, 'Tour in barca per ammirare la costa e le isole, tipico della Costiera Amalfitana.'),
('Passeggiata in gondola a Venezia', 1, 12, 'Romantica gita in gondola attraverso i canali di Venezia, unesperienza unica e indimenticabile.'),
('Opera al teatro di Verona', 1, 13, 'Assisti a uno spettacolo d opera all aperto nel teatro romano di Verona, un esperienza unica al tramonto.'),
('Giro in kayak nelle Grotte di Castellana', 3, 2, 'un complesso di grotte carsiche situate nel cuore della Puglia'),
('Escursionismo in montagna', 3, 1, 'Escursioni a piedi o in bicicletta per ammirare la bellezza naturale delle montagne italiane'),
('Arrampicata su roccia', 5, 8, 'Scalata di pareti rocciose in alcune delle zone più belle d Italia'),
('Tour in Vespa', 1, 14, 'Divertiti ad esplorare la città assieme alla passione dei motori'),
('Visita al Duomo di Milano', 1, 10, 'uno dei più grandi e splendidi edifici gotici al mondo.');

-- Inserimento delle categorie
INSERT INTO categorie (nome) VALUES
('Mare'),
('Montagna'),
('Citta');

-- Inserimento dei luoghi
INSERT INTO luoghi (nome, stato, longitudine, latitudine) 
VALUES
('Monte Bianco', 'Italia', 45.8325, 6.8650), -- Luogo di montagna
('Pirenei', 'Francia', 42.6611, 0.3328), -- Luogo di montagna
('Mediterraneo', 'Mare', 35.0000, 18.0000), -- Luogo di mare
('Parigi', 'Francia', 48.8566, 2.3522), -- Luogo di città
('Londra', 'Regno Unito', 51.5074, -0.1278), -- Luogo di città
('Tanzania', 'Tanzania', -6.3690, 34.8888), -- Luogo di mare
('Kenya', 'Kenya', 0.0236, 37.9062), -- Luogo di mare
('Maldive', 'Maldive', 3.2028, 73.2207), -- Luogo di mare
('Cannes', 'Francia', 43.5528, 7.0174), -- Luogo di città
('posto', 'Stati Uniti', 37.8651, -119.5383), -- Luogo di montagna
('Roma', 'Italia', 41.8933203, 12.4829321), -- Luogo di città
('Firenze', 'Italia', 43.7698712, 11.2555757), -- Luogo di città
('Amalfio', 'Italia', 40.63367, 14.6026095), -- Luogo di mare
('Venezia', 'Italia', 45.4371908, 12.3345898), -- Luogo di mare e città
('Verona', 'Italia', 45.4384958, 10.9924122), -- Luogo di città
('Torre dell orso', 'Italia', 40.2745056, 18.4301456), -- Luogo di mare
('Dolomiti', 'Italia', 46.294572, 12.0513238), -- Luogo di montagna
('Lago di Garda', 'Italia', 45.6613187, 10.6851043), -- Luogo di montagna
('Bologna', 'Italia', 44.4938203, 11.3426327), -- Luogo di città
('Milano', 'Italia', 45.4641943, 9.1896346); -- Luogo di città

-- Inserimento delle associazioni utenti-itinerari
INSERT INTO utenti_itinerari (id_utente, id_itinerario) VALUES
(1, 1), -- Alice - Esplorando le Alpi
(2, 3), -- Bob - Spiagge e Relax
(3, 7), -- Charlie - Viaggio tra i Borghi Medievali
(4, 6), -- Daniel - Camminando per la Costa Amalfitana
(5, 9), -- Emma - Navigando tra le Isole Greche
(6, 4), -- Frank - Scoprendo la Toscana
(7, 8), -- Grace - Tour Enogastronomico nel Piemonte
(8, 2), -- Harry - Città d'Arte Italiane
(9, 5); -- Isabella - Tesori del Sud

-- Inserimento delle associazioni attività-itinerari
INSERT INTO attivita_itinerari (id_attivita, id_itinerario) VALUES
(1, 1), -- Escursione sul Monte Bianco - Esplorando le Alpi
(2, 1), -- Trekking nei Pirenei - Esplorando le Alpi
(3, 3), -- Nuotata al mare - Spiagge e Relax
(4, 3), -- Lezione di nuoto sincronizzato - Spiagge e Relax
(5, 7), -- Visita al Louvre - Tour Enogastronomico nel Piemonte
(6, 7), -- Tour guidato del British Museum - Tour Enogastronomico nel Piemonte
(7, 4), -- Corso di cucina italiana - Scoprendo la Toscana
(8, 4), -- Corso di pasticceria francese - Scoprendo la Toscana
(9, 6), -- Safari in Tanzania - Camminando per la Costa Amalfitana
(10, 6), -- Safari fotografico in Kenya - Camminando per la Costa Amalfitana
(11, 9), -- Snorkeling alle Maldive - Navigando tra le Isole Greche
(12, 9), -- Escursione in barca a vela - Navigando tra le Isole Greche
(13, 1), -- Ciclismo in montagna - Esplorando le Alpi
(14, 7), -- Tour in bicicletta delle cantine - Tour Enogastronomico nel Piemonte
(15, 8), -- Scalata su roccia - Viaggio tra i Borghi Medievali
(16, 8), -- Lezione di arrampicata indoor - Viaggio tra i Borghi Medievali
(17, 9), -- Camping nel Parco Nazionale Yosemite - Navigando tra le Isole Greche
(18, 9); -- Escursione notturna con il fuoco - Navigando tra le Isole Greche

-- Inserimento delle associazioni attività-luoghi
INSERT INTO attivita_luoghi (id_attivita, id_luogo) VALUES
(1, 1), -- Escursione sul Monte Bianco - Monte Bianco
(2, 2), -- Trekking nei Pirenei - Pirenei
(3, 3), -- Nuotata al mare - Mediterraneo
(4, 9), -- Lezione di nuoto sincronizzato - Cannes
(5, 4), -- Visita al Louvre - Parigi
(6, 5), -- Tour guidato del British Museum - Londra
(7, 6), -- Corso di cucina italiana - Tanzania
(8, 6), -- Corso di pasticceria francese - Tanzania
(9, 6), -- Safari in Tanzania - Tanzania
(10, 7), -- Safari fotografico in Kenya - Kenya
(11, 8), -- Snorkeling alle Maldive - Maldive
(12, 8), -- Escursione in barca a vela - Maldive
(13, 1), -- Ciclismo in montagna - Monte Bianco
(14, 7), -- Tour in bicicletta delle cantine - Kenya
(15, 10), -- Scalata su roccia - Yosemite National Park
(16, 10), -- Lezione di arrampicata indoor - Yosemite National Park
(17, 10), -- Camping nel Parco Nazionale Yosemite - Yosemite National Park
(18, 10), -- Escursione notturna con il fuoco - Yosemite National Park
(19, 11), -- Esplora le aree sotterranee e scopri la storia di Roma.
(20, 11), -- Impara a maneggiare le armi utilizzate dai gladiatori nellantica Roma.
(21, 12), -- Impara a fare la pasta perfetta da chef locali.
(22, 12), -- Scopri la campagna toscana e le piccole comunità che si trovano tra i borghi medievali.
(23, 12), -- Bagno termale nelle acque termali naturali, per rilassarsi e rigenerarsi.
(24, 13), -- Tour in barca per ammirare la costa e le isole, tipico della Costiera Amalfitana.
(25, 14), -- Romantica gita in gondola attraverso i canali di Venezia, unesperienza unica e indimenticabile.
(26, 15), -- Assisti a uno spettacolo d'opera all'aperto nel teatro romano di Verona, un'esperienza unica al tramonto.
(27, 16), -- un complesso di grotte carsiche situate nel cuore della Puglia.
(28, 17), -- Escursioni a piedi o in bicicletta per ammirare la bellezza naturale delle montagne italiane
(29, 18), -- Scalata di pareti rocciose in alcune delle zone più belle d Italia
(30, 19), -- Divertiti ad esplorare la città assieme alla passione dei motori
(31, 20); -- uno dei più grandi e splendidi edifici gotici al mondo.

-- Inserimento delle associazioni luoghi-categorie
INSERT INTO luoghi_categorie (id_luogo, id_categoria) VALUES
(1, 2), -- Monte Bianco - Montagna
(2, 2), -- Pirenei - Montagna
(3, 1), -- Mediterraneo - Mare
(4, 3), -- Parigi - Città
(5, 3), -- Londra - Città
(6, 1), -- Tanzania - Mare
(7, 1), -- Kenya - Mare
(8, 1), -- Maldive - Mare
(9, 3), -- Cannes - Città
(10, 2), -- Yosemite National Park - Montagna
(11, 3), -- Roma - Città
(11, 3), -- Roma - Città
(12, 3), -- Firenze - Città
(12, 3), -- Firenze - Città
(12, 3), -- Firenze - Città
(13, 3), -- Amalfio - Città
(14, 3), -- Venezia - Città
(14, 1), -- Venezia - Mare
(15, 3), -- Venezia - Città
(16, 1), -- Torre dell orso - Mare
(17, 2), -- Dolomiti - Montagna
(18, 2), -- Lago di Garda - Montagna
(19, 2), -- Bologna - Montagna
(20, 3); -- Milano - Montagna
