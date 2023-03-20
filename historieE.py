# En bruker skal kunne registrere seg i kunderegisteret. Denne funksjonaliteten skal programmeres.

import sqlite3
import re

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
    print(f'\nNavn: {navn}, E-post: {epost}, Telefon: {telefon}\n')


navn = input('Angi navn: ')

while len(navn.split(" ")) <= 1: #Sjekker at navnet består av fornavn og etternavn
    print('Ugyldig navn')
    navn = input('Angi navn: ')


epost = input('Angi epost: ')

cursor.execute('SELECT Epost from KundeRegister')
epost_database = cursor.fetchall()

for i in range(len(epost_database)):
    epost_database[i] = epost_database[i][0]

while '@' not in epost or check_contains(epost, epost_database): #Sjekker at eposten er gyldig
    print('Ugyldig epost')
    epost = input('Angi epost: ')


pattern = re.compile(r'^[4-9]\d{7}$')
telefon = input('Angi telefon (Begynner på 4 eller 9, ellers åtte siffer langt): ')

cursor.execute('SELECT Mobilnummer from KundeRegister')
telefon_database = cursor.fetchall()

for i in range(len(telefon_database)):
    telefon_database[i] = telefon_database[i][0]

while not bool(pattern.match(telefon)) or check_contains(telefon, telefon_database): #Sjekker at telefonnummeret er gyldig
    print('Ugyldig telefon')
    telefon = input('Angi telefon: ')
    

insert_into(navn, epost, telefon)


con.close()
