# For en bruker skal man kunne finne all informasjon om de kjøpene hen har gjort for fremtidige
# reiser. Denne funksjonaliteten skal programmeres.

import sqlite3
import re

con = sqlite3.connect('tog2.db')

cursor = con.cursor()

def kjop_info(mobilnummer):
    cursor.execute('''
    SELECT * FROM KundeRegister 
	JOIN KundeOrdre USING(KundeID) 
	JOIN OrdrePaRute USING(OrdreNR) 
	JOIN TogTur USING(TogruteID) 
	JOIN Billett USING(OrdreNR)
	
	WHERE Mobilnummer = ?''', (mobilnummer))

    return cursor.fetchall


pattern = re.compile(r'^\d{8}$')
mobilnummer = input('Angi telefon: ')

while not bool(pattern.match(mobilnummer)): #Sjekker at telefonnummeret er gyldig
    print('Ugyldig telefon')
    mobilnummer = input('Angi telefon: ')

print(kjop_info(mobilnummer))