# Registrerte kunder skal kunne finne ledige billetter for en oppgitt strekning på en ønsket togrute
# og kjøpe de billettene hen ønsker. Denne funksjonaliteten skal programmeres.
# • Pass på at dere bare selger ledige plasser

import sqlite3
import re

gyldige_stasjoner = ['Trondheim', 'Steinkjer', 'Mosjøen', 'Mo i Rana', 'Fauske', 'Bodø']

start = input('Startstasjon: ')

while start not in gyldige_stasjoner: #Sjekker at startstasjonen er gyldig
    print('Ugyldig stasjon')
    start = input('Angi startstasjon: ')

slutt = input('Sluttstasjon: ')

while (slutt not in gyldige_stasjoner) and (start != slutt): #Sjekker at sluttstasjonen er gyldig
    print('Ugyldig stasjon')
    slutt = input('Angi sluttstasjon: ')

pattern1 = re.compile(r'\d{2}-\d{2}-\d{4}$')

dato = input('Dato (dd-mm-yyyy): ')

while not bool(pattern1.match(dato)): #Sjekker at dato er gyldig
    print('Ugyldig dato')
    dato = input('Angi ny dato: ')

pattern2 = re.compile(r'\d{2}:\d{2}$')

kl = input('Tidspunkt (hh:mm): ')

while not bool(pattern2.match(kl)): #Sjekker at klokkeslett er gyldig
    print('Ugyldig tidspunkt')
    kl = input('Angi nytt tidspunkt: ')

gyldige_typer = ['sete', 'seng']

# Her hentes vognoppsettet ut

if (vognopsett = natt):
    type = input('Ønsker du sete eller seng? ')
    if (type == 'seng'):
        plasser = input('Ønsker du én eller to plasser (1/2)? ')





