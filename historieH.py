# For en bruker skal man kunne finne all informasjon om de kjøpene hen har gjort for fremtidige
# reiser. Denne funksjonaliteten skal programmeres.

import sqlite3
import re
from datetime import date

con = sqlite3.connect('tog2.db')

cursor = con.cursor()

def kjop_info(mobilnummer, dato):
    cursor.execute('''
    SELECT * FROM KundeRegister 
	JOIN KundeOrdre USING(KundeID) 
	JOIN OrdrePaRute USING(OrdreNR) 
	JOIN TogTur USING(TogruteID) 
	JOIN Billett USING(OrdreNR)
	
	WHERE Mobilnummer = ? AND TogTur.Dato >= ?''', (mobilnummer, dato))

    return cursor.fetchall


pattern = re.compile(r'^\d{8}$')
mobilnummer = input('Angi telefon: ')

while not bool(pattern.match(mobilnummer)): #Sjekker at telefonnummeret er gyldig
    print('Ugyldig telefon')
    mobilnummer = input('Angi telefon: ')

dato = date.today()

print(kjop_info(mobilnummer, dato))