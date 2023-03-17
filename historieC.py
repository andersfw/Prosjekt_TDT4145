# For en stasjon som oppgis, skal bruker få ut alle togruter som er innom stasjonen en gitt ukedag.
# Denne funksjonaliteten skal programmeres.

import sqlite3

dag = input('Angi dag: ')

gyldige_dager = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag', 'Søndag']

while dag not in gyldige_dager:
    print('Ugyldig dag')
    dag = input('Angi dag: ')

station = input('Angi stasjon: ')

gyldige_stasjoner = ['Trondheim', 'Steinkjer', 'Mosjøen', 'Mo i Rana', 'Fauske', 'Bodø']

while station not in gyldige_stasjoner:
    print('Ugyldig stasjon')
    station = input('Angi stasjon: ')



con = sqlite3.connect('tog.db')

cursor = con.cursor()

cursor.execute('''SELECT DISTINCT Togrute.Navn FROM 
Togrute INNER JOIN TogTur ON Togrute.TogruteID = TogTur.TogruteID 
INNER JOIN PaDelstrekning ON Togrute.TogruteID = PaDelstrekning.TogruteID 
INNER JOIN Delstrekning ON PaDelstrekning.DelstrekningID = Delstrekning.DelstrekningID
WHERE Dag = ? AND (StartStasjon = ? OR SluttStasjon = ?)''', (dag, station, station))

rows = [row[0] for row in cursor.fetchall()]

for line in rows:
    print(line)