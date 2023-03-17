# En bruker skal kunne registrere seg i kunderegisteret. Denne funksjonaliteten skal programmeres.

import sqlite3

con = sqlite3.connect('db.db')

cursor = con.cursor()

cursor.execute("INSERT INTO KundeRegister VALUES (NULL,'Ola Nordmann','hei@heisann.no','12343378')")

