# En bruker skal kunne registrere seg i kunderegisteret. Denne funksjonaliteten skal programmeres.

import sqlite3
import re

def main(db):
    con = sqlite3.connect(db)

    cursor = con.cursor()

    def check_contains(param, lst):
        for i in lst:
            if param == i:
                return True
        return False

    def insert_into(navn, epost, telefon):
        cursor.execute('''INSERT INTO KundeRegister VALUES(NULL,?,?,?)'''
                    ,(navn, epost, telefon)) #KundeID er satt som autoincrement, derfor NULL
        
        con.commit()
        print('\n!Kunde registrert!')
        print(f'\nNavn: {navn}, E-post: {epost}, Telefon: {telefon}')


    pattern_navn = re.compile(r'^[a-zA-ZæøåÆØÅ]{2,} [a-zA-ZæøåÆØÅ]{2,}$') # regex for validering av navn 
    navn = input('Angi navn: ')

    while not bool(pattern_navn.match(navn)): #Sjekker at navnet er gyldig
        print('Ugyldig navn, skriv fullt navn')
        navn = input('Angi navn: ')


    pattern_epost = re.compile(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$') # regex for validering av epost
    epost = input('Angi epost: ')
    
    cursor.execute('SELECT Epost from KundeRegister') # Henter ut alle eposter fra databasen, for å sjekke om eposten finnes fra før

    epost_database = [row[0] for row in cursor.fetchall()]

    while not bool(pattern_epost.match(epost)) or (bool(pattern_epost.match(epost)) and check_contains(epost, epost_database)): #Sjekker at eposten er gyldig
        print('Ugyldig epost-format, eller eposten finnes fra før')
        epost = input('Angi epost: ')


    pattern_tlf = re.compile(r'^[4-9]\d{7}$') # regex for validering av telefonnummer
    telefon = input('Angi telefon (Begynner på 4 eller 9, ellers åtte siffer langt): ')

    cursor.execute('SELECT Mobilnummer from KundeRegister') # Henter ut alle telefonnummer fra databasen, for å sjekke om telefonnummeret finnes fra før
    telefon_database = [row[0] for row in cursor.fetchall()]

    while not bool(pattern_tlf.match(telefon)) or (bool(pattern_tlf.match(telefon)) and check_contains(telefon, telefon_database)): #Sjekker at telefonnummeret er gyldig
        print('Ugyldig telefon, eller finnes fra før')
        telefon = input('Angi telefon: ')
        
    # Kjører, etter alle valideringer, metoden som legger inn kunden i databasen
    insert_into(navn, epost, telefon) 


    con.close()

    return telefon
