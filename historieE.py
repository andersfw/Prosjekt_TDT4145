# En bruker skal kunne registrere seg i kunderegisteret. Denne funksjonaliteten skal programmeres.

import sqlite3

navn = input('Angi navn: ')

while len(navn.split(" ")) <= 1:
    print('Ugyldig navn')
    navn = input('Angi navn: ')

epost = input('Angi epost: ')

while '@' not in epost:
    print('Ugyldig epost')
    epost = input('Angi epost: ')

telefon = input('Angi telefon: ')

while len(telefon) != 8:
    print('Ugyldig telefon')
    telefon = input('Angi telefon: ')

con = sqlite3.connect('tog2.db')

cursor = con.cursor()

cursor.execute("INSERT INTO KundeRegister VALUES(NULL,?,?,?)",(navn, epost, telefon))

con.commit()
con.close()