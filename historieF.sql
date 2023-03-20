-- Billett Mobanen dag
INSERT INTO Billett VALUES (1, 1, 'Mo i Rana', 'Trondheim', 1, NULL, 1);

-- Kundeordre
INSERT INTO KundeOrdre VALUES (1, '2023-04-02', '10:15', 1);

-- OrdrePaRute
INSERT INTO OrdrePaRute VALUES (1, '2023-04-03', 3);

-- Billett(BillettID, OrdreNR, StartStasjon, SluttStasjon, SeteNR, SengNR, VognID)

-- KundeOrdre(OrdreNR, Dato, Tidspunkt, KundeID)

-- OrdrePaRute(OrdreNR, Dato, TogruteID)
