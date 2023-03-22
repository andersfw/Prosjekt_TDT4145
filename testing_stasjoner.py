import sqlite3

con = sqlite3.connect('tog8.db')

cursor = con.cursor()

start = input('Startstasjon: ')
slutt = input('Sluttstasjon: ')

cursor.execute('''
SELECT * FROM Delstrekning
WHERE StartStasjon = ? AND SluttStasjon = ?''',(start, slutt))

print(cursor.fetchall())