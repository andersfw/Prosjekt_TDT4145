
--Legger inn en kunde i systemet
INSERT INTO KundeRegister VALUES(1, 'SQ Lite', 'sq@lite.no', '44444444');

-- Billetten blir del av denne kundeordren, knyttet til kunden med kundeID = 1
INSERT INTO KundeOrdre VALUES (1, '2023-04-02', '10:15', 1);

-- Billett kjøpes Mo i Rana -> Trondheim dag
INSERT INTO Billett VALUES (1, 1, 'Mo i Rana', 'Trondheim', 1, NULL, 1);


-- Kundeordren knyttes til den aktuelle togruten på riktig dato
INSERT INTO OrdrePaRute VALUES (1, '2023-04-03', 3);



