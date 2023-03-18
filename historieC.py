# For en stasjon som oppgis, skal bruker få ut alle togruter som er innom stasjonen en gitt ukedag.
# Denne funksjonaliteten skal programmeres.

import sqlite3

dag = input('Angi dag: ')

gyldige_dager = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag', 'Søndag']

while dag not in gyldige_dager: #Sjekker at dagen er gyldig
    print('Ugyldig dag')
    dag = input('Angi dag: ')

stasjon = input('Angi stasjon: ')

gyldige_stasjoner = ['Trondheim', 'Steinkjer', 'Mosjøen', 'Mo i Rana', 'Fauske', 'Bodø']

while stasjon not in gyldige_stasjoner: #Sjekker at stasjonen er gyldig
    print('Ugyldig stasjon')
    stasjon = input('Angi stasjon: ')



con = sqlite3.connect('tog4.db')

cursor = con.cursor()

cursor.execute('''SELECT DISTINCT Togrute.Navn FROM 
Togrute INNER JOIN TogTur ON Togrute.TogruteID = TogTur.TogruteID 
INNER JOIN PaDelstrekning ON Togrute.TogruteID = PaDelstrekning.TogruteID 
INNER JOIN Delstrekning ON PaDelstrekning.DelstrekningID = Delstrekning.DelstrekningID
WHERE Dag = ? AND (StartStasjon = ? OR SluttStasjon = ?)''', (dag, stasjon, stasjon))

rows = [row[0] for row in cursor.fetchall()]
print(f'Togrutene som er innom {stasjon} på {dag} er:')
for i in range(len(rows)):
    print(f'[{i+1}] {rows[i]}')

con.close()