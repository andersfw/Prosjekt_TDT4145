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
INSERT INTO Operator VALUES('VY');

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


--Inn i Vogn

INSERT INTO Vogn VALUES(1, 'SJ');
INSERT INTO Vogn VALUES(2, 'SJ');
INSERT INTO Vogn VALUES(3, 'SJ');
INSERT INTO Vogn VALUES(4, 'SJ');
INSERT INTO Vogn VALUES(5, 'VY');
INSERT INTO Vogn VALUES(6, 'VY');
INSERT INTO Vogn VALUES(7, 'VY');
INSERT INTO Vogn VALUES(8, 'VY');


--Inn i Sete

--Vogn 1
INSERT INTO Sete VALUES(1,1);
INSERT INTO Sete VALUES(2,1);
INSERT INTO Sete VALUES(3,1);
INSERT INTO Sete VALUES(4,1);
INSERT INTO Sete VALUES(5,1);
INSERT INTO Sete VALUES(6,1);
INSERT INTO Sete VALUES(7,1);
INSERT INTO Sete VALUES(8,1);
INSERT INTO Sete VALUES(9,1);
INSERT INTO Sete VALUES(10,1);
INSERT INTO Sete VALUES(11,1);
INSERT INTO Sete VALUES(12,1);

--Vogn 2
INSERT INTO Sete VALUES(1,2);
INSERT INTO Sete VALUES(2,2);
INSERT INTO Sete VALUES(3,2);
INSERT INTO Sete VALUES(4,2);
INSERT INTO Sete VALUES(5,2);
INSERT INTO Sete VALUES(6,2);
INSERT INTO Sete VALUES(7,2);
INSERT INTO Sete VALUES(8,2);
INSERT INTO Sete VALUES(9,2);
INSERT INTO Sete VALUES(10,2);
INSERT INTO Sete VALUES(11,2);
INSERT INTO Sete VALUES(12,2);


--Inn i Seng

--Vogn 3
INSERT INTO Seng VALUES(1,3,1);
INSERT INTO Seng VALUES(2,3,1);
INSERT INTO Seng VALUES(3,3,2);
INSERT INTO Seng VALUES(4,3,2);
INSERT INTO Seng VALUES(5,3,3);
INSERT INTO Seng VALUES(6,3,3);
INSERT INTO Seng VALUES(7,3,4);
INSERT INTO Seng VALUES(8,3,4);

--Vogn 4
INSERT INTO Seng VALUES(1,4,1);
INSERT INTO Seng VALUES(2,4,1);
INSERT INTO Seng VALUES(3,4,2);
INSERT INTO Seng VALUES(4,4,2);
INSERT INTO Seng VALUES(5,4,3);
INSERT INTO Seng VALUES(6,4,3);
INSERT INTO Seng VALUES(7,4,4);
INSERT INTO Seng VALUES(8,4,4);

--Mangler Billett, KundeOrdre, KundeRegister, 
--PaDelstrekning, RutePaBane, Togrute, TogTur, VognOppsett