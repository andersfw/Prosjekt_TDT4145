# For en bruker skal man kunne finne all informasjon om de kjøpene hen har gjort for fremtidige
# reiser. Denne funksjonaliteten skal programmeres.

import sqlite3
import re
from datetime import date

con = sqlite3.connect('tog2.db')

cursor = con.cursor()

def check_contains(param, lst):
    for i in lst:
        if param == i:
            return True
    return False

def kjop_info(mobilnummer, dato):
    cursor.execute('''
    SELECT * FROM KundeRegister 
	JOIN KundeOrdre USING(KundeID) 
	JOIN OrdrePaRute USING(OrdreNR) 
	JOIN TogTur USING(TogruteID) 
	JOIN Billett USING(OrdreNR)
	
	WHERE Mobilnummer = ? AND TogTur.Dato >= ?''', (mobilnummer, dato))

    return cursor.fetchall()


pattern = re.compile(r'^[4-9]\d{7}$')
mobilnummer = input('Angi telefon (Begynner på 4 eller 9, ellers åtte siffer langt): ')

cursor.execute('SELECT Mobilnummer from KundeRegister')
telefon_database = cursor.fetchall()

for i in range(len(telefon_database)):
    telefon_database[i] = telefon_database[i][0]

while not check_contains(mobilnummer,telefon_database): #Sjekker om telefonnummeret er i databasen, trenger ikke
                                                        #validering her, da nummeret er validert ved input i E
    print('Ugyldig; nummeret finnes ikke i databasen:(')
    mobilnummer = input('Angi telefon: ')


dato = date.today()

print(kjop_info(mobilnummer, dato))