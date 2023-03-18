# Bruker skal kunne søke etter togruter som går mellom en startstasjon og en sluttstasjon, med
# utgangspunkt i en dato og et klokkeslett. Alle ruter den samme dagen og den neste skal
# returneres, sortert på tid. Denne funksjonaliteten skal programmeres.

import sqlite3
import re

gyldige_stasjoner = ['Trondheim', 'Steinkjer', 'Mosjøen', 'Mo i Rana', 'Fauske', 'Bodø']

start = input('Startstasjon: ')

while start not in gyldige_stasjoner: #Sjekker at startstasjonen er gyldig
    print('Ugyldig stasjon')
    start = input('Angi startstasjon: ')

slutt = input('Sluttstasjon: ')

while (slutt not in gyldige_stasjoner) and (start != slutt): #Sjekker at sluttstasjonen er gyldig
    print('Ugyldig stasjon')
    slutt = input('Angi sluttstasjon: ')

pattern1 = re.compile(r'\d{2}-\d{2}-\d{4}$')

dato = input('Dato (dd-mm-yyyy): ')

while not bool(pattern1.match(dato)): #Sjekker at dato er gyldig
    print('Ugyldig dato')
    dato = input('Angi ny dato: ')

pattern2 = re.compile(r'\d{2}:\d{2}$')

kl = input('Tidspunkt (hh:mm): ')

while not bool(pattern2.match(kl)): #Sjekker at klokkeslett er gyldig
    print('Ugyldig tidspunkt')
    kl = input('Angi nytt tidspunkt: ')


con = sqlite3.connect('tog2.db')

cursor = con.cursor()

cursor.execute('''SELECT * FROM

	Delstrekning JOIN PaDelstrekning USING(DelstrekningID)
	JOIN Togrute USING(TogruteID)
	JOIN TogTur USING(TogruteID)
	

WHERE (StartStasjon = ? OR SluttStasjon = ?) AND Dato = ?


GROUP BY TogruteID HAVING count(DelstrekningID)/2;''', (start, slutt, dato))

print(cursor.fetchall())

con.close()