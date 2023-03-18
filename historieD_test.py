# Bruker skal kunne søke etter togruter som går mellom en startstasjon og en sluttstasjon, med
# utgangspunkt i en dato og et klokkeslett. Alle ruter den samme dagen og den neste skal
# returneres, sortert på tid. Denne funksjonaliteten skal programmeres.

import sqlite3


con = sqlite3.connect('tog2.db')

cursor = con.cursor()


def ikke_nabostasjoner(start, slutt, dato):
    cursor.execute('''SELECT * FROM

        Delstrekning JOIN PaDelstrekning USING(DelstrekningID)
        JOIN Togrute USING(TogruteID)
        JOIN TogTur USING(TogruteID)
    WHERE (StartStasjon = ? OR SluttStasjon = ?) AND Dato = ?


    GROUP BY TogruteID HAVING count(DelstrekningID)/2;''',(start, slutt, dato))

    return cursor.fetchall()

def nabostasjoner(start, slutt, dato):

    cursor.execute('''SELECT * FROM

        Delstrekning JOIN PaDelstrekning USING(DelstrekningID)
        JOIN Togrute USING(TogruteID)
        JOIN TogTur USING(TogruteID)
	

        WHERE (StartStasjon = ? AND SluttStasjon = ?) AND Dato = ?''', (start, slutt, dato))
    
    return cursor.fetchall();


start = input('Angi startstasjon: ')

slutt = input('Angi sluttstasjon: ')

start_indeks = 0
slutt_indeks = 0
stasjoner = ['Trondheim', 'Steinkjer', 'Mosjøen', 'Mo i Rana', 'Fauske', 'Bodø']

for i in range(len(stasjoner)):
    if stasjoner[i] == start:
        start_indeks = i
    if stasjoner[i] == slutt:
        slutt_indeks = i

diff = abs(slutt_indeks - start_indeks)

print(diff)

dato = input('Angi dato (yyyy-mm-dd): ')


if diff == 1:

    print(nabostasjoner(start, slutt, dato))
else:
    print(ikke_nabostasjoner(start, slutt, dato))


con.close()