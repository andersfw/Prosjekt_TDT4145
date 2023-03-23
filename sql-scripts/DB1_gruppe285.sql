CREATE TABLE Jernbanestasjon(
	Navn VARCHAR(20),
	Hoyde VARCHAR(5),
	
	CONSTRAINT jbs_pk PRIMARY KEY(Navn)
);

CREATE TABLE Delstrekning(
	DelstrekningID INTEGER NOT NULL,
	Lengde INTEGER,
	Antall_spor INTEGER,
	StartStasjon VARCHAR(20),
	SluttStasjon VARCHAR(20),
	CONSTRAINT ds_pk PRIMARY KEY(DelstrekningID),
	CONSTRAINT ds_jbs_fk1 FOREIGN KEY(StartStasjon) REFERENCES Jernbanestasjon(Navn)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT ds_jbs_fk1 FOREIGN KEY(SluttStasjon) REFERENCES Jernbanestasjon(Navn)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);


CREATE TABLE Banestrekning(
	BanestrekningID INTEGER NOT NULL,
	Navn VARCHAR(40),
	Fremdriftsenergi VARCHAR(20),
	Retning VARCHAR(30),
	CONSTRAINT bs_pk PRIMARY KEY(BanestrekningID)
);

CREATE TABLE InneholderStrekninger(
	BanestrekningID INTEGER NOT NULL,
	DelstrekningID INTEGER NOT NULL,
	CONSTRAINT is_pk PRIMARY KEY (BanestrekningID, DelstrekningID),
	CONSTRAINT is_bs_fk FOREIGN KEY (BanestrekningID) REFERENCES Banestrekning(BanestrekningID)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT is_ds_fk FOREIGN KEY (DelstrekningID) REFERENCES Delstrekning(DelstrekningID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE Operator(
	OperatorNavn VARCHAR(15) NOT NULL,
	CONSTRAINT operator_pk PRIMARY KEY(OperatorNavn)
);

CREATE TABLE KundeRegister(
	KundeID INTEGER NOT NULL,
	Navn VARCHAR(40),
	Epost VARCHAR(40) UNIQUE,
	Mobilnummer VARCHAR(8) UNIQUE,
	CONSTRAINT kr_pk PRIMARY KEY(KundeID AUTOINCREMENT)
);

CREATE TABLE KundeOrdre(
	OrdreNR INTEGER NOT NULL,
	Dato VARCHAR(10),
	Tid VARCHAR(5),
	KundeID INTEGER NOT NULL,
	CONSTRAINT ko_pk PRIMARY KEY (OrdreNR),
	CONSTRAINT ko_kr_fk FOREIGN KEY (KundeID) REFERENCES KundeRegister(KundeID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE Togrute(
	TogruteID INTEGER NOT NULL,
	OperatorNavn VARCHAR(20) NOT NULL,
	Avgangstid VARCHAR(5),
	Navn VARCHAR(40),
	BanestrekningID INTEGER NOT NULL,
	CONSTRAINT tr_pk PRIMARY KEY (TogruteID),
	CONSTRAINT tr_op_fk FOREIGN KEY (OperatorNavn) REFERENCES Operator(OperatorNavn)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT tt_bs_fk FOREIGN KEY (BanestrekningID) REFERENCES Banestrekning(BanestrekningID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE TogTur(
	Dato VARCHAR(10),
	TogruteID INTEGER NOT NULL,
	Dag VARCHAR(10),
	CONSTRAINT tt_pk PRIMARY KEY (Dato, TogruteID),
	CONSTRAINT tt_tr_fk FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE Vogn(
	VognID INTEGER NOT NULL,
	OperatorNavn VARCHAR(15) NOT NULL,
	CONSTRAINT vogn_pk PRIMARY KEY (VognID),
	CONSTRAINT vogn_op_fk FOREIGN KEY (OperatorNavn) REFERENCES Operator(OperatorNavn)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE Sete(
	SeteNR INTEGER NOT NULL,
	VognID INTEGER NOT NULL,
	CONSTRAINT sete_pk PRIMARY KEY (SeteNR, VognID),
	CONSTRAINT sete_vogn_fk FOREIGN KEY (VognID) REFERENCES Vogn(VognID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE Seng(
	SengNR INTEGER NOT NULL,
	VognID INTEGER NOT NULL,
	KupeNR INTEGER NOT NULL,
	CONSTRAINT seng_pk PRIMARY KEY (SengNR, VognID),
	CONSTRAINT seng_vogn_fk FOREIGN KEY (VognID) REFERENCES Vogn(VognID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE Billett(
	BillettID INTEGER NOT NULL,
	OrdreNR INTEGER NOT NULL,
	StartStasjon VARCHAR(20) NOT NULL, 
	SluttStasjon VARCHAR(20) NOT NULL,
	SeteNR INTEGER,
	SengNR INTEGER,
	VognID INTEGER NOT NULL,
	CONSTRAINT bil_pk PRIMARY KEY (BillettID AUTOINCREMENT),
	CONSTRAINT bil_ko_fk FOREIGN KEY (OrdreNR) REFERENCES KundeOrdre(OrdreNR)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT bil_jbs_fk1 FOREIGN KEY (StartStasjon) REFERENCES Jernbanestasjon(Navn)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT bil_jbs_fk2 FOREIGN KEY (SluttStasjon) REFERENCES Jernbanestasjon(Navn)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT bil_sete_fk FOREIGN KEY (SeteNR) REFERENCES Sete(SeteNR)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT bil_seng_fk FOREIGN KEY (SengNR) REFERENCES Seng(SengNR)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT bil_vogn_fk FOREIGN KEY (VognID) REFERENCES Vogn(VognID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE VognOppsett(
	VognID INTEGER NOT NULL,
	TogruteID INTEGER NOT NULL,
	TogVognNR INTEGER,
	TogVognNavn VARCHAR(30),
	CONSTRAINT vo_pk PRIMARY KEY (VognID, TogruteID),
	CONSTRAINT vo_vogn_fk FOREIGN KEY (VognID) REFERENCES Vogn(VognID)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT vo_tr_fk FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);


CREATE TABLE PaDelstrekning(
	TogruteID INTEGER NOT NULL,
	DelstrekningID INTEGER NOT NULL,
	Avgangstid VARCHAR(5),
	Ankomsttid VARCHAR(5),
	Retning INTEGER,	
	CONSTRAINT pd_pk PRIMARY KEY (TogruteID, DelstrekningID),
	CONSTRAINT pd_tr_fk FOREIGN KEY (TogruteID) REFERENCES Togrute(TogruteID)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT pd_ds_fk FOREIGN KEY (DelstrekningID) REFERENCES Delstrekning(DelstrekningID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

CREATE TABLE OrdrePaRute(
	OrdreNR INTEGER NOT NULL,
	Dato VARCHAR(10) NOT NULL,
	TogruteID INTEGER NOT NULL,
	CONSTRAINT opr_pk PRIMARY KEY (OrdreNR,Dato, TogruteID),
	CONSTRAINT opr_tt_fk1 FOREIGN KEY (Dato) REFERENCES TogTur(Dato)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT opr_tt_fk2 FOREIGN KEY (TogruteID) REFERENCES TogTur(TogruteID)
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	CONSTRAINT opr_ko_fk FOREIGN KEY (OrdreNR) REFERENCES KundeOrdre(OrdreNR)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);

