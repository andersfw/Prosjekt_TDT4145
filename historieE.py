# En bruker skal kunne registrere seg i kunderegisteret. Denne funksjonaliteten skal programmeres.

import sqlite3

con = sqlite3.connect('db1.db')

cursor = con.cursor()

cursor.execute("SELECT * FROM KundeRegister")

print(cursor.fetchall())

