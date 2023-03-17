# En bruker skal kunne registrere seg i kunderegisteret. Denne funksjonaliteten skal programmeres.

import sqlite3
import re

navn = input('Angi navn: ')

while len(navn.split(" ")) <= 1: #Sjekker at navnet består av fornavn og etternavn
    print('Ugyldig navn')
    navn = input('Angi navn: ')

epost = input('Angi epost: ')

while '@' not in epost: #Sjekker at eposten er gyldig
    print('Ugyldig epost')
    epost = input('Angi epost: ')

pattern = re.compile(r'^\d{8}$')
telefon = input('Angi telefon: ')

while not bool(pattern.match(telefon)): #Sjekker at telefonnummeret er gyldig
    print('Ugyldig telefon')
    telefon = input('Angi telefon: ')

con = sqlite3.connect('tog2.db')

cursor = con.cursor()

cursor.execute("INSERT INTO KundeRegister VALUES(NULL,?,?,?)",(navn, epost, telefon)) #KundeID er satt som autoincrement, derfor NULL

con.commit()
con.close()