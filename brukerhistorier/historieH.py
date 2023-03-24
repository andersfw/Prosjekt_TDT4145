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
        SELECT KundeRegister.Navn, Mobilnummer, Epost, OrdreNR, Startstasjon, Sluttstasjon,
        Togtur.Dato, SeteNR, SengNR, TogVognNr, TogVognNavn, KundeOrdre.Dato, Tid 
        FROM KundeOrdre
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
            if row[8] == None:
                
                res += f'''
                Navn: {row[0]}, Mobilnummer: {row[1]}, E-post: {row[2]}, OrdreNR: {row[3]},
                Har bestilt reise fra {row[4]} til {row[5]} på dato {row[6]}, SeteNR: {row[7]}, VognNR i oppsett: {row[9]}, Vogntype: {row[10]}.
                Reisen ble bestilt {row[11]} klokken {row[12]}.
                '''
            if row[7] == None:
                res += f'''
                Navn: {row[0]}, Mobilnummer: {row[1]}, E-post: {row[2]}, OrdreNR: {row[3]},
                Har bestilt reise fra {row[4]} til {row[5]} på dato {row[6]}, SengNR: {row[8]}, KupéNR: {math.ceil(int(row[8])/2)}, VognNR i oppsett: {row[9]}, Vogntype: {row[10]}.
                Reisen ble bestilt {row[11]} klokken {row[12]}.
                '''
        return res

        # Ville egentlig her hente ut KupéNR direkte fra databasen, men siden sqlite3 ikke støtter right join, valgte vi math.ceil for å få kupéNR

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


