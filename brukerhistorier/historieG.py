# Registrerte kunder skal kunne finne ledige billetter for en oppgitt strekning på en ønsket togrute
# og kjøpe de billettene hen ønsker. Denne funksjonaliteten skal programmeres.
# • Pass på at dere bare selger ledige plasser

import sqlite3
import re
from brukerhistorier.historieD import *
from datetime import datetime, timedelta
import brukerhistorier.historieE as historieE
import time


def main(db):
    con = sqlite3.connect(db)

    cursor = con.cursor()

    def hentPlasseringer(TogruteID):  # Henter ut sete-/sengeplasser fra togruten
        cursor.execute('''SELECT VognOppsett.TogVognNR, Sete.SeteNR, Seng.SengNR, VognOppsett.VognID
            FROM Togrute
            INNER JOIN VognOppsett ON Togrute.TogruteID = VognOppsett.TogruteID
            INNER JOIN Vogn ON VognOppsett.VognID = Vogn.VognID
            LEFT JOIN Sete ON Vogn.VognID = Sete.VognID
            LEFT JOIN Seng ON Vogn.VognID = Seng.VognID
            WHERE Togrute.TogruteID = ?;''', (TogruteID))

        return cursor.fetchall()

    def hentBilletter(TogruteID, Dato):  # Henter ut alle billettene knyttet til en togtur
        cursor.execute('''SELECT VognOppsett.TogVognNR, Billett.SeteNR, Billett.SengNR, OrdrePaRute.TogruteID, Billett.StartStasjon, Billett.SluttStasjon
            FROM Billett JOIN OrdrePaRute ON Billett.OrdreNR = OrdrePaRute.OrdreNR
            JOIN (Togrute
            INNER JOIN VognOppsett ON Togrute.TogruteID = VognOppsett.TogruteID
            INNER JOIN Vogn ON VognOppsett.VognID = Vogn.VognID
            LEFT JOIN Sete ON Vogn.VognID = Sete.VognID
            LEFT JOIN Seng ON Vogn.VognID = Seng.VognID) ON 
            ((Sete.SeteNR = Billett.SeteNR OR Seng.SengNR = Billett.SengNR) AND 
            (Sete.VognID = Billett.VognID OR Seng.VognID = Billett.VognID)
            AND OrdrePaRute.TogruteID = Togrute.TogruteID)
            WHERE (OrdrePaRute.TogruteID = ? AND Dato = ?);''', (TogruteID, Dato))

        return cursor.fetchall()

    def hentStasjoner(TogruteID):
        cursor.execute('''SELECT PaDelstrekning.TogruteID, PaDelstrekning.DelstrekningID, Delstrekning.DelstrekningID, 
            Delstrekning.StartStasjon, Delstrekning.SluttStasjon
            FROM PaDelstrekning INNER JOIN Delstrekning USING(DelstrekningID)
            WHERE PaDelstrekning.TogruteID = ?''', (TogruteID))

        stash = cursor.fetchall()
        stasjoner = [row[3] for row in stash]
        stasjoner.append(stash[-1][-1])
        return stasjoner

    def sjekkOmMellomStasjoner(startStasjonNy, sluttStasjonNy, startStasjonGammel, sluttStasjonGammel, TogruteID):
        alle_stasjoner = hentStasjoner(TogruteID)
        stasjoner_ny = []
        start_indeks = alle_stasjoner.index(startStasjonNy)

        # Henter alle stasjonene som er mellom en gitt start- og sluttstasjon
        for i in range(start_indeks, len(alle_stasjoner)):
            stasjoner_ny.append(alle_stasjoner[i])
            if alle_stasjoner[i] == sluttStasjonNy:
                break

        stasjoner_gammel = []
        start_indeks = alle_stasjoner.index(startStasjonGammel)
        for i in range(start_indeks, len(alle_stasjoner)):
            stasjoner_gammel.append(alle_stasjoner[i])
            if alle_stasjoner[i] == sluttStasjonGammel:
                break

        return fellesStasjon(stasjoner_ny, stasjoner_gammel)

    def fellesStasjon(ny, gammel):
        result = 0
        for x in ny:
            for y in gammel:
                # hvis felles stasjon
                if x == y:
                    result += 1
        return result > 1

    # Legger inn en ny bestilling KUN DEMO-VERDIER NÅ
    def leggInnOrdre(OrdreNR, DatoBestilling, KlBestilling, KundeID, DatoTur, TogruteID):

        cursor.execute('''INSERT INTO KundeOrdre
        VALUES (?, ?, ?, ?);''', (str(OrdreNR), str(DatoBestilling), str(KlBestilling), str(KundeID)))

        con.commit()

        cursor.execute('''INSERT INTO OrdrePaRute
        VALUES (?, ?, ?);''', (OrdreNR, DatoTur, str(TogruteID)))

        con.commit()

    # Legger inn en ny bestilling KUN DEMO-VERDIER NÅ
    def leggInnBestilling(OrdreNR, StartStasjon, SluttStasjon, SeteNR, SengNR, VognID):

        cursor.execute('''INSERT INTO Billett
        VALUES (NULL, ?, ?, ?, ?, ?, ?);''', (OrdreNR, StartStasjon, SluttStasjon, SeteNR, SengNR, VognID))

        con.commit()

    # Henter antall ledige sete-/sengeplasser på en togtur
    def hentLedigePlasser(TogruteID, Dato, StartStasjonNy, SluttStasjonNy):
        ledigePlasseringer = hentPlasseringer(TogruteID)
        billetter = hentBilletter(TogruteID, Dato)
        ledige_senger = []
        ledige_seter = []
        for p in ledigePlasseringer:
            if p[1] != None:
                ledige_seter.append(p)
            elif p[2] != None:
                ledige_senger.append(p)
        for e in billetter:
            if e[1] != None:  # hvis billetten og plasseringen har samme TogVognNR
                for sete in ledige_seter:
                    # Sjekker om det er overlapp mellom stasjoner på billetten og det som bestilles, hvis ikke beholder den plasseringen
                    if e[1] == sete[1] and e[0] == sete[0] and sjekkOmMellomStasjoner(StartStasjonNy, SluttStasjonNy, e[4], e[5], TogruteID):
                        ledige_seter.remove(sete)
            elif e[2] != None:
                for seng in ledige_senger:
                    if e[2] == seng[2] and e[0] == seng[0]:
                        next_index = ledige_senger.index(seng)
                        ledige_senger.remove(seng)
                        if e[2] in [1, 3, 5, 7]:
                            ledige_senger.pop(next_index)

        ledigePlasseringer = []
        ledigePlasseringer.extend(ledige_seter)
        ledigePlasseringer.extend(ledige_senger)

        ledig = [0, 0]
        for x in ledigePlasseringer:
            if x[1] != None:
                ledig[0] += 1
            elif x[2] != None:
                ledig[1] += 1

        return ledig, ledigePlasseringer

    # Skriver ut de mulig avgangene i et oversiktlig format
    def printResultater(res, start, slutt):
        for i in range(len(res)):
            ledig, ledigePlasseringer = hentLedigePlasser(
                str(res[i][5]), res[i][13], start, slutt)
            print(f'\n[{i+1}] {res[i][11]} fra {start} til {slutt} kl. {res[i][6]}, {res[i][14]} {res[i][13]}.\n\t\tLedige sitteplasser: {ledig[0]}. Ledige sengeplasser: {ledig[1]}')
        print(f'\n[{len(res)+1}] Avbryt')

    def bestillPlasser(ordreNR, antall_sete, antall_seng, togruteID, dato_tur, start, slutt):
        cursor.execute(
            '''SELECT KundeID FROM KundeRegister WHERE Mobilnummer = ?''', (mobil,))
        kundeID = [row[0] for row in cursor.fetchall()]
        kundeID = kundeID[0]

        ledig, ledigePlasseringer = hentLedigePlasser(
            str(togruteID), dato_tur, start, slutt)
        kl_bestilling = datetime.now().strftime('%H:%M')
        dato_bestilling = datetime.now().strftime('%Y-%m-%d')

        if antall_sete > 0 or antall_seng > 0:
            leggInnOrdre(ordreNR, dato_bestilling, kl_bestilling,
                         kundeID, dato_tur, togruteID)

        for i in range(antall_sete):
            for p in range(len(ledigePlasseringer)):
                if ledigePlasseringer[p][1] != None:
                    leggInnBestilling(
                        ordreNR, start, slutt, ledigePlasseringer[p][1], None, ledigePlasseringer[p][3])
                    ledigePlasseringer.pop(p)
                    break
        for i in range(antall_seng):
            for p in range(len(ledigePlasseringer)):
                if ledigePlasseringer[p][2] != None:
                    leggInnBestilling(
                        ordreNR, start, slutt, None, ledigePlasseringer[p][2], ledigePlasseringer[p][3])
                    ledigePlasseringer.pop(p)
                    break

    def printBekreftelse(res, tur, start, slutt):
        time.sleep(1)
        print('\n')
        print(
            f'Da har du bestilt: {res[tur][11]} fra {start} til {slutt} kl. {res[tur][6]}, {res[tur][14]} {res[tur][13]}.')
        print('Gå til billett-oversikten for å se billettene dine.')
        print('\n')

    cursor.execute('SELECT Navn FROM Jernbanestasjon;')
    gyldige_stasjoner = [row[0] for row in cursor.fetchall()]

    print('\n')

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
    WHERE StartStasjon = ? AND SluttStasjon = ?;''', (start, slutt))

    nabo_res = cursor.fetchall()

    if nabo_res != []:
        nabo = True
    else:
        nabo = False

    pattern1 = re.compile(r'\d{4}-\d{2}-\d{2}$')

    dato = input('Dato (yyyy-mm-dd): ')

    # Sjekker at dato er gyldig
    while not bool(pattern1.match(dato)):
        print('Ugyldig dato')
        dato = input('Angi ny dato: ')

    pattern2 = re.compile(r'\d{2}:\d{2}$')

    kl = input('Tidspunkt (hh:mm): ')

    # Sjekker at klokkeslett er gyldig
    while not bool(pattern2.match(kl)):
        print('Ugyldig tidspunkt')
        kl = input('Angi nytt tidspunkt: ')

    res = hentResultater(start, slutt, dato, kl, nabo, cursor)
    print('\nAvganger:')
    time.sleep(1)
    printResultater(res, start, slutt)

    print('\n')

    pattern3 = re.compile(r'\d{1,2}$')

    tur = input('Hvilken avgang ønsker du å bestille? ')
    # Sjekker at svaret er gyldig
    while not bool(pattern3.match(tur)) or int(tur) < 1 or len(res)+1 < int(tur):
        tur = input('Svaret må være et av tall-alternativene over: ')

    if int(tur) == len(res)+1:
        return
    tur = int(tur) - 1

    ledig, ledigePlasser = hentLedigePlasser(
        str(res[tur][5]), res[tur][13], start, slutt)
    ordreNR = datetime.now().strftime('%f')
    cursor.execute('''SELECT Mobilnummer FROM KundeRegister;''')
    kunder = [str(row[0]) for row in cursor.fetchall()]
    mobil = ''

    while mobil not in kunder:
        print('\nEr du:')
        print('[1] Ny kunde')
        print('[2] Eksisterende kunde')
        kunde_type = input('Svar: ')
        # Sjekker at svaret er gyldig
        while not bool(pattern3.match(kunde_type)) or int(kunde_type) < 1 or 2 < int(kunde_type):
            kunde_type = input('Svar: ')
        print('\n')
        if kunde_type == '1':
            mobil = historieE.main(db)
            break
        elif kunde_type == '2':
            mobil = input('Angi ditt mobilnummer: ')
            if mobil not in kunder:
                print('\nFinner ikke mobilnummeret.\n')
                time.sleep(2)
    print('\n')

    togruteID = res[tur][5]
    dato_tur = res[tur][13]

    # Sjekker om man må velge mellom sete/seng, evt om det er ingen ledige plasser
    if ledig[0] == 0 and ledig[1] == 0:
        print('Det er ingen ledige plasser på denne togturen.')
    elif ledig[1] == 0:
        sitteplasser = input('Hvor mange sitteplasser ønsker du? ')
        while not bool(pattern3.match(sitteplasser)) or int(sitteplasser) > ledig[0] or int(sitteplasser) < 0:
            sitteplasser = input(
                'Det er ikke nok ledige seter igjen. Velg et nytt antall: ')
        bestillPlasser(ordreNR, int(sitteplasser), 0,
                       togruteID, dato_tur, start, slutt)
        printBekreftelse(res, tur, start, slutt)
    elif ledig[0] == 0:
        sengeplasser = input('Hvor mange sengeplasser ønsker du? ')
        while not bool(pattern3.match(sengeplasser)) or int(sengeplasser) > ledig[1] or int(sengeplasser) < 0:
            sengeplasser = input(
                'Det er ikke nok ledige seter igjen. Velg et nytt antall: ')
        bestillPlasser(ordreNR, 0, int(sengeplasser),
                       togruteID, dato_tur, start, slutt)
        printBekreftelse(res, tur, start, slutt)
    else:
        pattern4 = re.compile(r'\d{1,2},\d{1,2}$')
        antall = input('Hvor mange seter og senger ønsker du? (seter,senger) ')
        # Sjekker at svaret er gyldig
        while not bool(pattern4.match(antall)) or int(antall[0]) > ledig[0] or int(antall[0]) < 0 or int(antall[2]) > ledig[1] or int(antall[2]) < 0:
            antall = input(
                'Svaret må være på formen "antall seter, antall senger": ')
        bestillPlasser(ordreNR, int(antall[0]), int(
            antall[2]), togruteID, dato_tur, start, slutt)
        printBekreftelse(res, tur, start, slutt)

    con.close()

    time.sleep(2)

# Er alle sovevogner alltid 8 senger/4 kupeer?
