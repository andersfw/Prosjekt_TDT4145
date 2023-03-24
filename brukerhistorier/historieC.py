# For en stasjon som oppgis, skal bruker få ut alle togruter som er innom stasjonen en gitt ukedag.
# Denne funksjonaliteten skal programmeres.

import sqlite3

def main(db):
    con = sqlite3.connect(db)
    dag = input('Angi dag: ')
    cursor = con.cursor()

    gyldige_dager = ['Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag', 'Søndag']

    while dag not in gyldige_dager: #Sjekker at dagen er gyldig, altså en av ukedagene
        print('Ugyldig dag')
        dag = input('Angi dag: ')

    stasjon = input('Angi stasjon: ')

    cursor.execute('SELECT Navn from Jernbanestasjon') 
    gyldige_stasjoner = [row[0] for row in cursor.fetchall()] #Henter ut alle stasjoner fra databasen
    
    while stasjon not in gyldige_stasjoner: #Sjekker at stasjonen er gyldig
        print('Ugyldig stasjon')
        stasjon = input('Angi stasjon: ')

    # Spørringen under vil returnere alle togruter som har en togtur på en gitt dag der delstrekningen
    # har stasjonen som enten start- eller sluttstasjon
    cursor.execute('''SELECT DISTINCT Togrute.Navn FROM Togrute
    JOIN TogTur USING (TogruteID) 
    JOIN PaDelstrekning USING (TogruteID) 
    JOIN Delstrekning USING (DelstrekningID)
    WHERE Dag = ? AND (StartStasjon = ? OR SluttStasjon = ?)''', (dag, stasjon, stasjon))

    rows = [row[0] for row in cursor.fetchall()] # Moderer resultatet fra spørringen til en liste med kun informasjonen som trengs
    print(f'Togrutene som er innom {stasjon} på {dag} er:') # Skriver ut resultatet på en fin, leselig måte
    for i in range(len(rows)):
        print(f'[{i+1}] {rows[i]}')

    con.close()
