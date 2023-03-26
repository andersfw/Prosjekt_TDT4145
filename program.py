import brukerhistorier.historieC as historieC
import brukerhistorier.historieD as historieD
import brukerhistorier.historieE as historieE
import brukerhistorier.historieG as historieG
import brukerhistorier.historieH as historieH

db = 'tog.db'

print('\nVelkommen til togdatabasen!')

print('Dine valg i programmet er:')

alternativer = '''
C - Søk etter ruter langs en bestemt stasjon
D - Finn alle avganger for to påfølgende dager mellom 2 stasjoner
E - Registrer ny kunde
G - Finn og kjøp billetter
H - Finn din reisehistorikk\n
Q - Avslutte applikasjon\n'''

print(alternativer)

gyldige_valg = ['c', 'd', 'e', 'g', 'h', 'q']
valg = input('Hva vil du gjøre: (Skriv inn bokstav) ').lower()

while valg != 'q':
    while valg not in gyldige_valg:
        valg = input('Du må skrive inn en av bokstavene over: ').lower()

    if valg == 'c':
        historieC.main(db)
    elif valg == 'd':
        historieD.main(db)
    elif valg == 'e':
        historieE.main(db)
    elif valg == 'g':
        historieG.main(db)
    elif valg == 'h':
        historieH.main(db)
    else:
        break
    valg = input(f'\nTjeneste utført! Hva vil du gjøre nå?\n' +
                 alternativer + '\nVelg her: ').lower()

print('\nTakk for at du brukte togdatabasen!\n')
print('Restart programmet (pil opp) for å bruke det igjen.')
