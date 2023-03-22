# En bruker skal kunne registrere seg i kunderegisteret. Denne funksjonaliteten skal programmeres.

import sqlite3
import re

def main():
    con = sqlite3.connect('tog2.db')

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


    navn = input('Angi navn: ')

    while len(navn.split(" ")) <= 1: #Sjekker at navnet består av fornavn og etternavn
        print('Ugyldig navn')
        navn = input('Angi navn: ')


    epost = input('Angi epost: ')

    cursor.execute('SELECT Epost from KundeRegister')
    epost_database = [row[0] for row in cursor.fetchall()]

    while '@' not in epost or ('@' in epost and check_contains(epost, epost_database)): #Sjekker at eposten er gyldig
        print('Ugyldig epost, eller finnes fra før')
        epost = input('Angi epost: ')


    pattern = re.compile(r'^[4-9]\d{7}$')
    telefon = input('Angi telefon (Begynner på 4 eller 9, ellers åtte siffer langt): ')

    cursor.execute('SELECT Mobilnummer from KundeRegister')
    telefon_database = [row[0] for row in cursor.fetchall()]

    while not bool(pattern.match(telefon)) or (bool(pattern.match(telefon)) and check_contains(telefon, telefon_database)): #Sjekker at telefonnummeret er gyldig
        print('Ugyldig telefon, eller finnes fra før')
        telefon = input('Angi telefon: ')
        

    insert_into(navn, epost, telefon)


    con.close()
