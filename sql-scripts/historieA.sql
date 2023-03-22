-- Databasen skal kunne registrere data om alle jernbanestrekninger i Norge. Dere skal legge inn
-- data for Nordlandsbanen (som vist i figuren). Dette kan gjøres med et skript, dere trenger ikke å
-- programmere støtte for denne funksjonaliteten.

--Inn i Jernbanestasjon

INSERT INTO Jernbanestasjon VALUES('Trondheim','5,1');
INSERT INTO Jernbanestasjon VALUES('Steinkjer','3,6');
INSERT INTO Jernbanestasjon VALUES('Mosjøen','6,8');
INSERT INTO Jernbanestasjon VALUES('Mo i Rana','3,5');
INSERT INTO Jernbanestasjon VALUES('Fauske','34,0');
INSERT INTO Jernbanestasjon VALUES('Bodø','4,1');

--Inn i Delstrekning

INSERT INTO Delstrekning VALUES(1, 120,2,'Trondheim','Steinkjer');
INSERT INTO Delstrekning VALUES(2, 280,1,'Steinkjer','Mosjøen');
INSERT INTO Delstrekning VALUES(3, 90,1,'Mosjøen','Mo i Rana');
INSERT INTO Delstrekning VALUES(4, 170,1,'Mo i Rana','Fauske');
INSERT INTO Delstrekning VALUES(5, 60,1,'Fauske','Bodø');
INSERT INTO Delstrekning VALUES(6, 60,1,'Bodø', 'Fauske');
INSERT INTO Delstrekning VALUES(7, 170,1,'Fauske','Mo i Rana');
INSERT INTO Delstrekning VALUES(8, 90,1,'Mo i Rana','Mosjøen');
INSERT INTO Delstrekning VALUES(9, 280,1,'Mosjøen','Steinkjer');
INSERT INTO Delstrekning VALUES(10, 120,2,'Steinkjer','Trondheim');

--Inn i Operatør

INSERT INTO Operator VALUES('SJ');

--Inn i Banestrekning

INSERT INTO Banestrekning VALUES(1, 'Nordlandsbanen', 'Diesel', 'Trondheim -> Bodø');
INSERT INTO Banestrekning VALUES(2, 'Nordlandsbanen - motsatt', 'Diesel', 'Trondheim -> Bodø');



--Inn i InneholderStrekninger

--Nordlandsbanen
INSERT INTO InneholderStrekninger VALUES(1,1);
INSERT INTO InneholderStrekninger VALUES(1,2);
INSERT INTO InneholderStrekninger VALUES(1,3);
INSERT INTO InneholderStrekninger VALUES(1,4);
INSERT INTO InneholderStrekninger VALUES(1,5);

--Nordlandsbanen - motsatt
INSERT INTO InneholderStrekninger VALUES(2,6);
INSERT INTO InneholderStrekninger VALUES(2,7);
INSERT INTO InneholderStrekninger VALUES(2,8);
INSERT INTO InneholderStrekninger VALUES(2,9);
INSERT INTO InneholderStrekninger VALUES(2,10);
