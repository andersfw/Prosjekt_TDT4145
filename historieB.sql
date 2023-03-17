-- Dere skal kunne registrere data om togruter. Dere skal legge inn data for de tre togrutene på
-- Nordlandsbanen som er beskrevet i vedlegget til denne oppgave. Dette kan gjøres med et skript,
-- dere trenger ikke å programmere støtte for denne funksjonaliteten.

--Inn i Banestrekning

INSERT INTO Banestrekning VALUES(3, 'Mo-banen', 'Diesel', 'Mo i Rana -> Trondheim');

--Inn i InneholderStrekninger

--Mo-banen
INSERT INTO InneholderStrekninger VALUES(3,8);
INSERT INTO InneholderStrekninger VALUES(3,9);
INSERT INTO InneholderStrekninger VALUES(3,10);

--Inn i Togrute

--Nordlandsbanen dag
INSERT INTO Togrute VALUES(1, 'SJ', '07:49','Nordlandsbanen Dag',1);
--Nordlandsbanen natt
INSERT INTO Togrute VALUES(2, 'SJ', '23:05','Nordlandsbanen Natt',1);
--Mo-banen morgen
INSERT INTO Togrute VALUES(3, 'SJ', '08:11','Mobanen Morgen',3);

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


--Inn i Togrute

--Inn i VognOppsett

--Nordlandsbanen dag
INSERT INTO VognOppsett VALUES(1, 1, 1, 'SJ-sittevogn-1');
INSERT INTO VognOppsett VALUES(2, 1, 2, 'SJ-sittevogn-1');

--Nordlandsbanen natt
INSERT INTO VognOppsett VALUES(1, 2, 1, 'SJ-sittevogn-1');
INSERT INTO VognOppsett VALUES(3, 2, 2, 'SJ-sovevogn-1');

--Mo-banen morgen
INSERT INTO VognOppsett VALUES(1, 3, 1, 'SJ-sittevogn-1');

--Inn i PaDelstrekning

--Nordlandsbanen dag
INSERT INTO PaDelstrekning VALUES(1, 1, '09:51');
INSERT INTO PaDelstrekning VALUES(1, 2, '13:20');
INSERT INTO PaDelstrekning VALUES(1, 3, '14:31');
INSERT INTO PaDelstrekning VALUES(1, 4, '16:49');
INSERT INTO PaDelstrekning VALUES(1, 5, '17:34');

--Nordlandsbanen natt
INSERT INTO PaDelstrekning VALUES(2, 1, '00:57');
INSERT INTO PaDelstrekning VALUES(2, 2, '04:41');
INSERT INTO PaDelstrekning VALUES(2, 3, '05:55');
INSERT INTO PaDelstrekning VALUES(2, 4, '08:19');
INSERT INTO PaDelstrekning VALUES(2, 5, '09:05');

--Mo-banen morgen
INSERT INTO PaDelstrekning VALUES(3, 8, '09:14');
INSERT INTO PaDelstrekning VALUES(3, 9, '12:31');
INSERT INTO PaDelstrekning VALUES(3, 10, '14:13');
