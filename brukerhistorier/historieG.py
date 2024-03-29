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

    # Kobler til databasen 'db' som er satt i 'program.py'.
    con = sqlite3.connect(db)

    cursor = con.cursor()

    # Henter ut alle mulige sete- og sengeplasser fra togruten.
    def hentPlasseringer(TogruteID):
        cursor.execute('''SELECT VognOppsett.TogVognNR, Sete.SeteNR, Seng.SengNR, VognOppsett.VognID
            FROM Togrute
            INNER JOIN VognOppsett ON Togrute.TogruteID = VognOppsett.TogruteID
            INNER JOIN Vogn ON VognOppsett.VognID = Vogn.VognID
            LEFT JOIN Sete ON Vogn.VognID = Sete.VognID
            LEFT JOIN Seng ON Vogn.VognID = Seng.VognID
            WHERE Togrute.TogruteID = ?;''', (TogruteID))

        return cursor.fetchall()

    # Henter ut alle billettene knyttet til en togtur
    def hentBilletter(TogruteID, Dato):
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

    # Henter ut alle stasjonene på en togrute. Brukes kun i 'sjekkOmMellomStasjoner()'.
    def hentStasjoner(TogruteID):
        cursor.execute('''SELECT PaDelstrekning.TogruteID, PaDelstrekning.DelstrekningID, Delstrekning.DelstrekningID, 
            Delstrekning.StartStasjon, Delstrekning.SluttStasjon
            FROM PaDelstrekning INNER JOIN Delstrekning USING(DelstrekningID)
            WHERE PaDelstrekning.TogruteID = ?''', (TogruteID))

        stash = cursor.fetchall()
        stasjoner = [row[3] for row in stash]
        stasjoner.append(stash[-1][-1])
        return stasjoner

    # Sjekker om det er overlapp mellom to strekninger.
    # Dette er for å sjekke hvilke deler av en togrute en billett gjelder på i 'hentLedigePlasser()'
    def sjekkOmMellomStasjoner(StartStasjon_ny, SluttStasjon_ny, StartStasjon_gammel, SluttStasjon_gammel, TogruteID):
        alle_stasjoner = hentStasjoner(TogruteID)
        stasjoner_ny = []
        start_indeks = alle_stasjoner.index(StartStasjon_ny)

        # Henter alle stasjonene som er mellom en gitt start- og sluttstasjon
        for i in range(start_indeks, len(alle_stasjoner)):
            stasjoner_ny.append(alle_stasjoner[i])
            if alle_stasjoner[i] == SluttStasjon_ny:
                break

        stasjoner_gammel = []
        start_indeks = alle_stasjoner.index(StartStasjon_gammel)
        for i in range(start_indeks, len(alle_stasjoner)):
            stasjoner_gammel.append(alle_stasjoner[i])
            if alle_stasjoner[i] == SluttStasjon_gammel:
                break

        return fellesStasjon(stasjoner_ny, stasjoner_gammel)

    # Brukes som en hjelpefunksjon i sjekkOmMellomStasjoner.
    # Sjekker om de to listene med stasjoner har noen til felles.
    # Det går fint å ha én felles stasjon da én billett kan være til en stasjon,
    # og så er en annen billett videre fra den samme stasjonen.
    def fellesStasjon(ny, gammel):
        result = 0
        for x in ny:
            for y in gammel:
                # hvis felles stasjon
                if x == y:
                    result += 1
        return result > 1

    # Legger inn en KundeOrdre i databasen, samtidig som den oppdaterer OrdrePaRute,
    # som kun gjøres én gang per runde en kunde bestiller billetter.
    def leggInnOrdre(OrdreNR, dato_bestilling, kl_bestilling, KundeID, dato_tur, TogruteID):

        cursor.execute('''INSERT INTO KundeOrdre
        VALUES (?, ?, ?, ?);''', (str(OrdreNR), str(dato_bestilling), str(kl_bestilling), str(KundeID)))

        con.commit()

        cursor.execute('''INSERT INTO OrdrePaRute
        VALUES (?, ?, ?);''', (OrdreNR, dato_tur, str(TogruteID)))

        con.commit()

    # Legger inn en ny billett i databasen. Dette skjer for hver plass på togruten som bestilles,
    # altså flere ganger per kundeordre dersom det er bestilt flere antall plasser.
    def leggInnBestilling(OrdreNR, StartStasjon, SluttStasjon, SeteNR, SengNR, VognID):

        cursor.execute('''INSERT INTO Billett
        VALUES (NULL, ?, ?, ?, ?, ?, ?);''', (OrdreNR, StartStasjon, SluttStasjon, SeteNR, SengNR, VognID))

        con.commit()

    # Henter antall ledige sete- og sengeplasser på en togtur.
    # Dette gjøres ved å hente alle mulige plasser på en togrute vha. hentPlasseringer(),
    # for så å fjerne plasser dersom det eksisterer en billett på samme togtur, vogn og plass.
    def hentLedigePlasser(TogruteID, Dato, StartStasjon_ny, SluttStasjon_ny):
        ledige_plasseringer = hentPlasseringer(TogruteID)
        billetter = hentBilletter(TogruteID, Dato)
        ledige_senger = []
        ledige_seter = []

        # Legger til alle sitteplasser i én liste, og alle sengeplasser i en annen,
        # for å enklere kunne håndtere forskjellene i egenskapene til de to plass-typene.
        for p in ledige_plasseringer:
            if p[1] != None:
                ledige_seter.append(p)
            elif p[2] != None:
                ledige_senger.append(p)

        for b in billetter:
            # Hvis billetten er en sete-billett
            if b[1] != None:
                for sete in ledige_seter:
                    # Sjekker først om seteNR på billetten og på plassen er det samme.
                    # Sjekker så at vognNR på billetten og på plassen er det samme.
                    # Sjekker til slutt om det er overlapp mellom stasjoner på billetten og det som bestilles, hvis ikke beholder den plasseringen.
                    if b[1] == sete[1] and b[0] == sete[0] and sjekkOmMellomStasjoner(StartStasjon_ny, SluttStasjon_ny, b[4], b[5], TogruteID):
                        # Hvis if-setningen er sann, vil setet bli fjernet fra ledige_seter, som da tilsier at det blir fjernet fra ledige_plasseringer.
                        ledige_seter.remove(sete)
            # Hvis billetten er en seng-billett
            elif b[2] != None:
                for seng in ledige_senger:
                    # Sjekker først om sengNR på billetten og på plassen er det samme.
                    # Sjekker så at vognNR på billetten og på plassen er det samme.
                    if b[2] == seng[2] and b[0] == seng[0]:
                        next_index = ledige_senger.index(seng)
                        # Hvis if-setningen er sann, vil sengen bli fjernet fra ledige_senger, som da tilsier at det blir fjernet fra ledige_plasseringer.
                        ledige_senger.remove(seng)
                        # Fjerner neste seng dersom den er i samme kupé som sengen i billetten.
                        if b[2] in [1, 3, 5, 7]:
                            ledige_senger.pop(next_index)

        # Legger sammen ledige seter og senger til en felles oversikt over alle ledige plasser.
        ledige_plasseringer = []
        ledige_plasseringer.extend(ledige_seter)
        ledige_plasseringer.extend(ledige_senger)

        # Finner antallet ledige seter og senger.
        ledig = [0, 0]
        for x in ledige_plasseringer:
            if x[1] != None:
                ledig[0] += 1
            elif x[2] != None:
                ledig[1] += 1

        return ledig, ledige_plasseringer

    # Skriver ut de mulig avgangene i et oversiktlig format
    def printResultater(res, start, slutt):
        for i in range(len(res)):
            ledig = hentLedigePlasser(
                str(res[i][5]), res[i][13], start, slutt)[0]
            print(f'\n[{i+1}] {res[i][11]} fra {start} til {slutt} kl. {res[i][6]}, {res[i][14]} {res[i][13]}.\n\t\tLedige sitteplasser: {ledig[0]}. Ledige sengeplasser: {ledig[1]}')
        print(f'\n[{len(res)+1}] Avbryt')

    # Setter sammen bestillingen og legger inn kundeordre og riktig antall billetter.
    def bestillPlasser(ordreNR, antall_sete, antall_seng, togruteID, dato_tur, start, slutt):
        cursor.execute(
            '''SELECT KundeID FROM KundeRegister WHERE Mobilnummer = ?''', (mobil,))
        kundeID = [row[0] for row in cursor.fetchall()]
        kundeID = kundeID[0]

        ledige_plasseringer = hentLedigePlasser(
            str(togruteID), dato_tur, start, slutt)[1]
        kl_bestilling = datetime.now().strftime('%H:%M')
        dato_bestilling = datetime.now().strftime('%Y-%m-%d')

        # Legger inn en kundeordre for hele bestillingen dersom det bestilles ett eller flere seter/senger.
        if antall_sete > 0 or antall_seng > 0:
            leggInnOrdre(ordreNR, dato_bestilling, kl_bestilling,
                         kundeID, dato_tur, togruteID)

        # Legger inn antall seter i bestillingen.
        for i in range(antall_sete):
            for p in range(len(ledige_plasseringer)):
                # Finner det første ledige setet og legger det til i bestillingen/billetten.
                if ledige_plasseringer[p][1] != None:
                    leggInnBestilling(
                        ordreNR, start, slutt, ledige_plasseringer[p][1], None, ledige_plasseringer[p][3])
                    ledige_plasseringer.pop(p)
                    break

        # Legger inn antall senger i bestillingen.
        for i in range(antall_seng):
            for p in range(len(ledige_plasseringer)):
                # Finner det første ledige sengen og legger det til i bestillingen/billetten.
                if ledige_plasseringer[p][2] != None:
                    leggInnBestilling(
                        ordreNR, start, slutt, None, ledige_plasseringer[p][2], ledige_plasseringer[p][3])
                    ledige_plasseringer.pop(p)
                    break

    # Skriver ut en bekreftelse på at man har lagt inn en bestilling på gitt togtur.
    def printBekreftelse(res, tur, start, slutt):
        time.sleep(1)
        print('\n')
        print(
            f'Da har du bestilt: {res[tur][11]} fra {start} til {slutt} kl. {res[tur][6]}, {res[tur][14]} {res[tur][13]}.')
        print('Gå til billett-oversikten for å se billettene dine.')
        print('\n')

    ### PROGRAM / INPUT ###

    # Brukes til å validere input fra brukeren.
    pattern1 = re.compile(r'\d{4}-\d{2}-\d{2}$')
    pattern2 = re.compile(r'\d{2}:\d{2}$')
    pattern3 = re.compile(r'\d{1,2}$')
    pattern4 = re.compile(r'\d{1,2},\d{1}$')

    cursor.execute('SELECT Navn FROM Jernbanestasjon;')
    gyldige_stasjoner = [row[0] for row in cursor.fetchall()]

    print('\n')

    start = input('Startstasjon: ')

    # Sjekker at startstasjonen er gyldig
    while start not in gyldige_stasjoner:
        print('Ugyldig stasjon')
        start = input('Angi startstasjon: ')

    slutt = input('Sluttstasjon: ')

    # Sjekker at sluttstasjonen er gyldig
    while (slutt not in gyldige_stasjoner) and (start != slutt):
        print('Ugyldig stasjon')
        slutt = input('Angi sluttstasjon: ')

    # Sjekker om de to stasjonene som er lagt inn er nabostasjoner, for å bruke det senere.
    cursor.execute('''
    SELECT * FROM Delstrekning
    WHERE StartStasjon = ? AND SluttStasjon = ?;''', (start, slutt))

    nabo_res = cursor.fetchall()

    if nabo_res != []:
        nabo = True
    else:
        nabo = False

    dato = input('Dato (yyyy-mm-dd): ')

    # Sjekker at dato er gyldig
    while not bool(pattern1.match(dato)):
        print('Ugyldig dato')
        dato = input('Angi ny dato: ')

    kl = input('Tidspunkt (hh:mm): ')

    # Sjekker at klokkeslett er gyldig
    while not bool(pattern2.match(kl)):
        print('Ugyldig tidspunkt')
        kl = input('Angi nytt tidspunkt: ')

    # Henter ut avgangene som matcher input-verdiene fra brukeren.
    res = hentResultater(start, slutt, dato, kl, nabo, cursor)
    print('\nAvganger:')
    time.sleep(1)
    printResultater(res, start, slutt)

    print('\n')

    tur = input('Hvilken avgang ønsker du å bestille? ')
    # Sjekker at svaret er gyldig
    while not bool(pattern3.match(tur)) or int(tur) < 1 or len(res)+1 < int(tur):
        tur = input('Svaret må være et av tall-alternativene over: ')

    # Avbryter og går tilbake til hovedmenyen dersom brukeren velger det siste alternativet på tur.
    if int(tur) == len(res)+1:
        return
    tur = int(tur) - 1

    togruteID = res[tur][5]
    dato_tur = res[tur][13]

    # Henter ut antallet ledige plasser på den avgangen brukeren valgte.
    ledig = hentLedigePlasser(
        str(togruteID), dato_tur, start, slutt)[0]
    ordreNR = datetime.now().strftime('%f')
    cursor.execute('''SELECT Mobilnummer FROM KundeRegister;''')
    kunder = [str(row[0]) for row in cursor.fetchall()]
    mobil = ''

    # Sjekker om mobilnummeret brukeren la inn eksisterer i kunderegisteret.
    # Hvis det ikke gjør det må brukeren registrere seg som en nye kunde.
    while mobil not in kunder:
        print('\nEr du:')
        print('[1] Ny kunde')
        print('[2] Eksisterende kunde')
        kunde_type = input('Svar: ')
        # Sjekker at svaret er gyldig
        while not bool(pattern3.match(kunde_type)) or int(kunde_type) < 1 or 2 < int(kunde_type):
            kunde_type = input('Svar: ')
        print('\n')
        # Går til kunderegistrering dersom kunden velger alt. 1.
        if kunde_type == '1':
            mobil = historieE.main(db)
            break
        elif kunde_type == '2':
            mobil = input('Angi ditt mobilnummer: ')
            if mobil not in kunder:
                print('\nFinner ikke mobilnummeret.\n')
                time.sleep(2)
    print('\n')

    # Sjekker om man må velge mellom sete/seng, evt om det er ingen ledige plasser

    # Hvis det ikke er noen ledige sete- eller sengeplasser igjen.
    if ledig[0] == 0 and ledig[1] == 0:
        print('Det er ingen ledige plasser på denne togturen.')
    # Dersom det ikke eksisterer sengeplasser eller ikke er noen ledige igjen.
    elif ledig[1] == 0:
        sitteplasser = input('Hvor mange sitteplasser ønsker du? ')
        while not bool(pattern3.match(sitteplasser)) or int(sitteplasser) > ledig[0] or int(sitteplasser) < 0:
            sitteplasser = input(
                'Det er ikke nok ledige seter igjen. Velg et nytt antall: ')
        bestillPlasser(ordreNR, int(sitteplasser), 0,
                       togruteID, dato_tur, start, slutt)
        printBekreftelse(res, tur, start, slutt)
    # Dersom det ikke eksisterer sitteplasser eller ikke er noen ledige igjen.
    elif ledig[0] == 0:
        sengeplasser = input('Hvor mange sengeplasser ønsker du? ')
        while not bool(pattern3.match(sengeplasser)) or int(sengeplasser) > ledig[1] or int(sengeplasser) < 0:
            sengeplasser = input(
                'Det er ikke nok ledige seter igjen. Velg et nytt antall: ')
        bestillPlasser(ordreNR, 0, int(sengeplasser),
                       togruteID, dato_tur, start, slutt)
        printBekreftelse(res, tur, start, slutt)
    # Dersom det både er ledige sitteplasser og sengeplasser.
    else:
        antall = input('Hvor mange seter og senger ønsker du? (seter,senger) ')
        plasser = antall.split(',')
        # Sjekker at svaret er gyldig
        while not bool(pattern4.match(antall)) or int(plasser[0]) > ledig[0] or int(plasser[0]) < 0 or int(plasser[1]) > ledig[1] or int(plasser[1]) < 0:
            antall = input(
                'Svaret må være på formen "antall seter, antall senger": ')
            plasser = antall.split(',')
        bestillPlasser(ordreNR, int(plasser[0]), int(
            plasser[1]), togruteID, dato_tur, start, slutt)
        printBekreftelse(res, tur, start, slutt)

    con.close()

    time.sleep(2)
