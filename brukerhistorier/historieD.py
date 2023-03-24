# Bruker skal kunne søke etter togruter som går mellom en startstasjon og en sluttstasjon, med
# utgangspunkt i en dato og et klokkeslett. Alle ruter den samme dagen og den neste skal
# returneres, sortert på tid. Denne funksjonaliteten skal programmeres.

import sqlite3
import re
from datetime import datetime, timedelta


# Denne spørringen gir oss delstrekningene som enten har startstasjonen vår som startstasjon eller
# sluttstasjonen vår som sluttstasjon. For å finne alle "riktige" svar grupperer vi derfor på TogruteID og Dato.
# Dersom antallet av delstrekninger i denne grupperingen er lik 2 betyr dette at vi har en riktig rute.
# Den andre delen av WHERE-betingelsen oppfyller oppgaveteksten, altså at vi skal finne alle ruter på dag1 som går etter
# klokkeslettet vi har oppgitt, og alle ruter på dag2.
# Vi sorterer deretter på dato og tid, slik at vi får riktig rekkefølge på svarene.
def ikke_nabostasjoner(start, slutt, dato, tid, dato_etter, cursor):

    retning = hentRetning(start, slutt)

    cursor.execute('''SELECT * FROM 
    
            Delstrekning JOIN PaDelstrekning USING(DelstrekningID) 
            JOIN Togrute USING(TogruteID) 
            JOIN TogTur USING(TogruteID)
        WHERE (StartStasjon = ? OR SluttStasjon = ?) AND                
        ((Dato = ? AND Togrute.Avgangstid >= ?) OR Dato = ?) AND PaDelstrekning.Retning = ?
        GROUP BY TogruteID,Dato HAVING count(DelstrekningID)/2
        ORDER BY Dato ASC, Togrute.Avgangstid ASC''', (start, slutt, dato, tid, dato_etter, retning))
    return cursor.fetchall()


# For nabostasjoner blir mye likt, men ettersom vi her kun vil ha EN delstrekning trenger vi en 'AND' i WHERE-betingelsen.
# Vi trenger følgelig ingen sjekk, ettersom vi er sikre på at det er rett resultat dersom startstasjon = start og
# sluttstasjon = slutt. Dato/tid - sjekk er samme som før og deretter sorteres det utifra oppgaveteksten.
def nabostasjoner(start, slutt, dato, tid, dato_etter, cursor):

    retning = hentRetning(start, slutt)

    cursor.execute('''SELECT * FROM
            Delstrekning JOIN PaDelstrekning USING(DelstrekningID)
            JOIN Togrute USING(TogruteID)
            JOIN TogTur USING(TogruteID)
    
        WHERE (StartStasjon = ? AND SluttStasjon = ?) AND 
        ((Dato = ? AND Togrute.Avgangstid >= ?) OR Dato = ?) AND PaDelstrekning.Retning = ?
        ORDER BY Dato ASC, Togrute.Avgangstid ASC''', (start, slutt, dato, tid, dato_etter, retning))
    return cursor.fetchall()


def hentRetning(start, slutt):

    stasjonsliste = ['Trondheim', 'Steinkjer',
                     'Mosjøen', 'Mo i Rana', 'Fauske', 'Bodø']
    start_index = stasjonsliste.index(start)
    slutt_index = stasjonsliste.index(slutt)
    diff = slutt_index - start_index

    if diff == abs(diff):
        return 1
    else:
        return 0


def hentResultater(start, slutt, dato, kl, nabo, cursor):
    res = []
    dato_etter = datetime.strptime(
        dato, '%Y-%m-%d').date() + timedelta(days=1)
    dato_etter = dato_etter.strftime('%Y-%m-%d')
    if nabo:  # Dersom stasjonene er naboer, vil vi ha resultatet fra metoden nabostasjoner
        res.extend(nabostasjoner(
            start, slutt, dato, kl, dato_etter, cursor))
    elif not nabo:  # Hvis de ikke er det, vil vi ha resultatet fra metoden ikke_nabostasjoner
        res.extend(ikke_nabostasjoner(
            start, slutt, dato, kl, dato_etter, cursor))
    return res


def printResultater(res, start, slutt):  # Formaterer resultatet på en fin, leselig måte
    for i in range(len(res)):
        print(
            f'[{i+1}] {res[i][11]} fra {start} til {slutt} kl. {res[i][6]}, {res[i][14]} {res[i][13]}.')


def main(db):
    con = sqlite3.connect(db)

    cursor = con.cursor()

    # Henter ut alle jernbanestasjoner fra databasen
    cursor.execute('SELECT Navn from Jernbanestasjon')
    gyldige_stasjoner = [row[0] for row in cursor.fetchall()]

    start = input('Startstasjon: ')

    while start not in gyldige_stasjoner:  # Sjekker at startstasjonen er gyldig
        print('Ugyldig stasjon')
        start = input('Angi startstasjon: ')

    slutt = input('Sluttstasjon: ')

    # Sjekker at sluttstasjonen er gyldig
    while (slutt not in gyldige_stasjoner) and (start != slutt):
        print('Ugyldig stasjon')
        slutt = input('Angi sluttstasjon: ')

    cursor.execute('''
    SELECT * FROM Delstrekning
    WHERE StartStasjon = ? AND SluttStasjon = ?''', (start, slutt))  # Denne metoden sjekker om stasjonene er naboer

    nabo_res = cursor.fetchall()

    if nabo_res != []:  # Dersom resultatet fra nabo-spørringen ga et resultat, vil stasjonene være naboer
        nabo = True
    else:
        nabo = False

    pattern1 = re.compile(r'\d{4}-\d{2}-\d{2}$')

    dato = input('Dato (yyyy-mm-dd): ')

    while not bool(pattern1.match(dato)):  # Sjekker at dato er gyldig
        print('Ugyldig dato')
        dato = input('Angi ny dato: ')

    pattern2 = re.compile(r'\d{2}:\d{2}$')

    kl = input('Tidspunkt (hh:mm): ')

    while not bool(pattern2.match(kl)):  # Sjekker at klokkeslett er gyldig
        print('Ugyldig tidspunkt')
        kl = input('Angi nytt tidspunkt: ')

    printResultater(hentResultater(start, slutt, dato, kl,
                    nabo, cursor), start, slutt)

    con.close()
