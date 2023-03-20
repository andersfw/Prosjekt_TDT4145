# Registrerte kunder skal kunne finne ledige billetter for en oppgitt strekning på en ønsket togrute
# og kjøpe de billettene hen ønsker. Denne funksjonaliteten skal programmeres.
# • Pass på at dere bare selger ledige plasser

import sqlite3
import re
from datetime import datetime, timedelta

con = sqlite3.connect('tog7.db')

cursor = con.cursor()

def ikke_nabostasjoner(start, slutt, dato, tid, dato_etter):
    cursor.execute('''SELECT * FROM 
    
            Delstrekning JOIN PaDelstrekning USING(DelstrekningID) 
            JOIN Togrute USING(TogruteID) 
            JOIN TogTur USING(TogruteID)

        WHERE (StartStasjon = ? OR SluttStasjon = ?) AND 
        ((Dato = ? AND PaDelstrekning.Avgangstid >= ?) OR Dato = ?)

        GROUP BY TogruteID,Dato HAVING count(DelstrekningID)/2;''', (start, slutt, dato, tid, dato_etter))

    return cursor.fetchall()

def nabostasjoner(start, slutt, dato, tid, dato_etter):

    cursor.execute('''SELECT * FROM

            Delstrekning JOIN PaDelstrekning USING(DelstrekningID)
            JOIN Togrute USING(TogruteID)
            JOIN TogTur USING(TogruteID)
	
        WHERE (StartStasjon = ? AND SluttStasjon = ?) AND 
        ((Dato = ? AND PaDelstrekning.Avgangstid >= ?) OR Dato = ?)''', (start, slutt, dato, tid, dato_etter))
    
    return cursor.fetchall()

def hentPlasseringer(TogruteID): # Henter ut sete-/sengeplasser fra togruten 
    cursor.execute('''SELECT VognOppsett.TogVognNR, Sete.SeteNR, Seng.SengNR
        FROM Togrute
        INNER JOIN VognOppsett ON Togrute.TogruteID = VognOppsett.TogruteID
        INNER JOIN Vogn ON VognOppsett.VognID = Vogn.VognID
        LEFT JOIN Sete ON Vogn.VognID = Sete.VognID
        LEFT JOIN Seng ON Vogn.VognID = Seng.VognID
        WHERE Togrute.TogruteID = ?;''', (TogruteID))

    return cursor.fetchall()

def hentBilletter(TogruteID, Dato): # Henter ut alle billettene knyttet til en togtur
    cursor.execute('''SELECT VognOppsett.TogVognNR, Billett.SeteNR, Billett.SengNR, OrdrePaRute.TogruteID
        FROM Billett JOIN OrdrePaRute ON Billett.OrdreNR = OrdrePaRute.OrdreNR
        JOIN (Togrute
        INNER JOIN VognOppsett ON Togrute.TogruteID = VognOppsett.TogruteID
        INNER JOIN Vogn ON VognOppsett.VognID = Vogn.VognID
        LEFT JOIN Sete ON Vogn.VognID = Sete.VognID
        LEFT JOIN Seng ON Vogn.VognID = Seng.VognID) ON 
        ((Sete.SeteNR = Billett.SeteNR OR Seng.SengNR = Billett.SengNR) AND 
        (Sete.VognID = Billett.VognID OR Seng.VognID = Billett.VognID)
        AND OrdrePaRute.TogruteID = Togrute.TogruteID)
        WHERE (OrdrePaRute.TogruteID = ? AND Dato = ?);''', (TogruteID, Dato))

    return cursor.fetchall()

def leggInnBestilling(OrdreNR, DatoBestilling, KlBestilling, KundeID, DatoTur, TogruteID, BillettID, StartStasjon, SluttStasjon, SeteNR, SengNR, VognID): # Legger inn en ny bestilling KUN DEMO-VERDIER NÅ
    
    cursor.execute('''INSERT INTO KundeOrdre
    VALUES (?, ?, ?, ?);''', (OrdreNR, DatoBestilling, KlBestilling, KundeID))

    cursor.execute('''INSERT INTO OrdrePaRute
    VALUES (?, ?, ?);''', (OrdreNR, DatoTur, TogruteID))

    cursor.execute('''INSERT INTO Billett
    VALUES (?, ?, ?, ?, ?, ?, ?);''', (BillettID, OrdreNR, StartStasjon, SluttStasjon, SeteNR, SengNR, VognID))

    con.commit()

def hentResultater(start, slutt, dato, kl): # Henter ut de mulige avgangene
    res = []
    dato_etter = datetime.strptime(dato, '%Y-%m-%d').date() + timedelta(days = 1)
    dato_etter = dato_etter.strftime('%Y-%m-%d')

    if nabostasjoner(start, slutt, dato, kl, dato_etter):
        res.extend(nabostasjoner(start, slutt, dato, kl, dato_etter))
    if ikke_nabostasjoner(start, slutt, dato, kl, dato_etter):
        res.extend(ikke_nabostasjoner(start, slutt, dato, kl, dato_etter))

    return res

def hentLedigePlasser(TogruteID, Dato): # Henter antall ledige sete-/sengeplasser på en togtur
    ledigePlasseringer = hentPlasseringer(TogruteID)
    billetter = hentBilletter(TogruteID, Dato)
    ledig = [0, 0]
    for e in billetter:
        for i in ledigePlasseringer:
            if e[0] == i[0]:
                if (e[1] == i[1] and e[1] != None) or (e[2] == i[2] and e[2] != None):
                    ledigePlasseringer.remove(i)

    for x in ledigePlasseringer:
        if x[1] != None:
            ledig[0] += 1
        elif x[2] != None:
            ledig[1] += 1 
    
    return ledig

def printResultater(res): # Skriver ut de mulig avgangene i et oversiktlig format
    for i in range(len(res)):
        ledig = hentLedigePlasser(str(res[i][5]), res[i][12])
        print(f'\n[{i+1}] {res[i][10]} fra {start} til {slutt} kl. {res[i][6]}, {res[i][13]} {res[i][12]}.\n\t\tLedige sitteplasser: {ledig[0]}. Ledige sengeplasser: {ledig[1]}')

# def hentPlasser():
    cursor.execute('''SELECT Togrute.TogruteID, 
        COUNT(SeteNR) AS AntallSeter, COUNT(SengNR) AS AntallSenger
        FROM Togrute
        JOIN VognOppsett ON Togrute.TogruteID = VognOppsett.TogruteID
        JOIN Vogn ON VognOppsett.VognID = Vogn.VognID
        LEFT JOIN Sete ON Vogn.VognID = Sete.VognID
        LEFT JOIN Seng ON Vogn.VognID = Seng.VognID
        WHERE Togrute.TogruteID = '2'
        GROUP BY Togrute.TogruteID;''')

    return cursor.fetchall()

# def hentLedigePlasser():
    cursor.execute('''SELECT Billett.SeteNR, Sete.SeteNR, Billett.SengNR, Seng.SengNR, OrdrePaRute.TogruteID, Togrute.TogruteID
      FROM Togrute
      INNER JOIN VognOppsett USING(TogruteID)
      INNER JOIN Vogn USING(VognID)
      LEFT JOIN Sete USING(VognID)
      LEFT JOIN Seng USING(VognID)
      INNER JOIN (Billett INNER JOIN OrdrePaRute USING(OrdreNR)) ON 
      (((Sete.SeteNR != Billett.SeteNR AND Sete.VognID = Billett.VognID) OR 
      (Seng.SengNR = Billett.SengNR AND Seng.VognID = Billett.VognID)) AND 
      OrdrePaRute.TogruteID = Togrute.TogruteID)
      WHERE (Togrute.TogruteID NOT IN (
    SELECT TogruteID
    FROM OrdrePaRute
    WHERE Dato = '2023-04-03'
        Dato = '2023-04-03');''')

      # OrdrePaRute.TogruteID = '3' AND 

    return cursor.fetchall()

gyldige_stasjoner = ['Trondheim', 'Steinkjer', 'Mosjøen', 'Mo i Rana', 'Fauske', 'Bodø']

start = input('Startstasjon: ')

while start not in gyldige_stasjoner: #Sjekker at startstasjonen er gyldig
    print('Ugyldig stasjon')
    start = input('Angi startstasjon: ')

slutt = input('Sluttstasjon: ')

while (slutt not in gyldige_stasjoner) and (start != slutt): #Sjekker at sluttstasjonen er gyldig
    print('Ugyldig stasjon')
    slutt = input('Angi sluttstasjon: ')

pattern1 = re.compile(r'\d{4}-\d{2}-\d{2}$')

dato = input('Dato (yyyy-mm-dd): ')


while not bool(pattern1.match(dato)): #Sjekker at dato er gyldig
    print('Ugyldig dato')
    dato = input('Angi ny dato: ')

pattern2 = re.compile(r'\d{2}:\d{2}$')

kl = input('Tidspunkt (hh:mm): ')

while not bool(pattern2.match(kl)): #Sjekker at klokkeslett er gyldig
    print('Ugyldig tidspunkt')
    kl = input('Angi nytt tidspunkt: ')

res = hentResultater(start, slutt, dato, kl)
printResultater(res)

print('\n')

pattern3 = re.compile(r'\d{1}$')

tur = input('Hvilken tur ønsker du å bestille? ')
while not bool(pattern3.match(tur)) or int(tur) < 1 or len(res) < int(tur): # Sjekker at svaret er gyldig
    tur = input('Svaret må være et av tall-alternativene over: ')

tur = int(tur) - 1

ledig = hentLedigePlasser(str(res[tur][5]), res[tur][12])

# Sjekker om man må velge mellom sete/seng, evt om det er ingen ledige plasser
if ledig[0] == 0 and ledig[1] == 0:
    print('Det er ingen ledige plasser på denne togturen.')
elif ledig[1] == 0:
    print('\n')
    print(f'Da har du bestilt: {res[tur][10]} fra {start} til {slutt} kl. {res[tur][6]}, {res[tur][13]} {res[tur][12]}.')
    print('Gå til billett-oversikten for å se billettene dine.')
    leggInnBestilling(datetime.now().strftime('%f'), datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M'), '1', res[tur][12], res[tur][5], datetime.now().strftime('%f'), start, slutt, '4', None, '1') # Denne legger kun inn demo-verdier, altså vil det ikke funke igjen med samme nøkler. KundeID, SeteNR og VognID må endres på
else:
    gyldige_typer = ['sete', 'seng']
    type = input('Ønsker du sete- eller sengeeplass? (sete/seng) ')
    while type.lower() not in gyldige_typer:
        type = input('Du må skrive inn sete eller seng: ')
    print('\n')
    print(f'Da har du bestilt: {res[tur][10]} fra {start} til {slutt} kl. {res[tur][6]}, {res[tur][13]} {res[tur][12]}.')
    print('Gå til billett-oversikten for å se billettene dine.')


con.close()

