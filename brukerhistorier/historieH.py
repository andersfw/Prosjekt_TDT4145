import datetime
import sqlite3
import re
import time
import math

dato = datetime.date.today()


def main(db):
    con = sqlite3.connect(db)

    cursor = con.cursor()
    # Hjelpemetode for å sjekke om et element er i en liste
    def check_contains(param, lst):
        for i in lst:
            if param == i:
                return True
        return False

    # Henter her ut alle kundeordrene til en kunde som er gjort for alle togruter som har avgang etter dagens dato
    # Kunden blir entydig identifisert gjennom mobilnummeret sitt, som vil oppgis og lagres som en variabel i programmet.
    def kjop_info(mobilnummer):
        cursor.execute('''
        SELECT * FROM KundeOrdre
        JOIN KundeRegister USING(KundeID)
        JOIN OrdrePaRute USING(OrdreNR)
        JOIN TogTur ON (TogTur.TogruteID = OrdrePaRute.TogruteID AND TogTur.Dato = OrdrePaRute.Dato)
        JOIN Billett USING(OrdreNR)
        JOIN Togrute USING(TogruteID)
        JOIN VognOppsett ON (VognOppsett.VognID = Billett.VognID AND VognOppsett.TogruteID = Togrute.TogruteID)

        WHERE Mobilnummer = ? AND TogTur.Dato >= ? ''', (mobilnummer, dato))

        print('\nBillettoversikt: ')
        result =  cursor.fetchall()
        res = ""
        for row in result:
            if row[16] == None:
                
                res += f'''
                Navn: {row[4]}, Mobilnummer: {row[6]}, E-post: {row[5]}, OrdreNR: {row[0]},
                Har bestilt reise fra {row[13]} til {row[14]} på dato {row[9]}, SeteNR: {row[15]}, VognNR: {row[24]}, Vogntype: {row[25]}.
                Reisen ble bestilt {row[1]} klokken {row[2]}.
                '''
            if row[15] == None:
                res += f'''
                Navn: {row[4]}, Mobilnummer: {row[6]}, E-post: {row[5]}, OrdreNR: {row[0]},
                Har bestilt reise fra {row[13]} til {row[14]} på dato {row[9]}, SengNR: {row[16]}, KupéNR: {math.ceil(int(row[16])/2)}, VognNR: {row[24]}, Vogntype: {row[25]}.
                Reisen ble bestilt {row[1]} klokken {row[2]}.
                '''
        return res


    mobilnummer = input('Angi telefon (Begynner på 4 eller 9, ellers åtte siffer langt): ')

    cursor.execute('SELECT Mobilnummer from KundeRegister')
    telefon_database = cursor.fetchall()

    for i in range(len(telefon_database)):
        telefon_database[i] = telefon_database[i][0]

    # Sjekker om telefonnummeret er i databasen, trenger ikke validering her, da nummeret er validert ved input i E
    while not check_contains(mobilnummer,telefon_database):  
        print('Ugyldig; nummeret finnes ikke i databasen:(')
        mobilnummer = input('Angi telefon: ')

    print(kjop_info(mobilnummer)) # Skriver ut alle kjøpene til kunden

    time.sleep(2)

    con.close()


