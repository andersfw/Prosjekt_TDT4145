# Bruker skal kunne søke etter togruter som går mellom en startstasjon og en sluttstasjon, med
# utgangspunkt i en dato og et klokkeslett. Alle ruter den samme dagen og den neste skal
# returneres, sortert på tid. Denne funksjonaliteten skal programmeres.

import sqlite3
import re
from datetime import datetime, timedelta

con = sqlite3.connect('tog4.db')

cursor = con.cursor()

def ikke_nabostasjoner(start, slutt, dato, tid, dato_etter):
    cursor.execute('''SELECT * FROM 
    
            Delstrekning JOIN PaDelstrekning USING(DelstrekningID) 
            JOIN Togrute USING(TogruteID) 
            JOIN TogTur USING(TogruteID)

        WHERE (StartStasjon = ? OR SluttStasjon = ?) AND 
        ((Dato = ? AND PaDelstrekning.Avgangstid >= ?) OR Dato = ?)

        GROUP BY TogruteID,Dato HAVING count(DelstrekningID)/2
        ORDER BY Dato ASC, PaDelstrekning.Avgangstid ASC''', (start, slutt, dato, tid, dato_etter))

    return cursor.fetchall()

def nabostasjoner(start, slutt, dato, tid, dato_etter):

    cursor.execute('''SELECT * FROM

            Delstrekning JOIN PaDelstrekning USING(DelstrekningID)
            JOIN Togrute USING(TogruteID)
            JOIN TogTur USING(TogruteID)
	

        WHERE (StartStasjon = ? AND SluttStasjon = ?) AND 
        ((Dato = ? AND PaDelstrekning.Avgangstid >= ?) OR Dato = ?)
        ORDER BY Dato ASC, PaDelstrekning.Avgangstid ASC''', (start, slutt, dato, tid, dato_etter))
    
    return cursor.fetchall()

def hentResultater(start, slutt, dato, kl):
    res = []
    dato_etter = datetime.strptime(dato, '%Y-%m-%d').date() + timedelta(days = 1)
    dato_etter = dato_etter.strftime('%Y-%m-%d')

    if nabostasjoner(start, slutt, dato, kl, dato_etter):
        res.extend(nabostasjoner(start, slutt, dato, kl, dato_etter))
    if ikke_nabostasjoner(start, slutt, dato, kl, dato_etter):
        res.extend(ikke_nabostasjoner(start, slutt, dato, kl, dato_etter))

    return res

def printResultater(res):
    for i in range(len(res)):
        print(f'[{i+1}] {res[i][10]} fra {start} til {slutt} kl. {res[i][6]}, {res[i][13]} {res[i][12]}.')


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

printResultater(hentResultater(start, slutt, dato, kl))

con.close()

