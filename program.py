import historieC
import historieD
import historieE
import historieG
import historieH

print('\n!¤#Velkommen til togdatabasen!¤#')

print('Dine valg i programmet er:')

print('''
C - Søk etter ruter langs en bestemt stasjon
D - Finn alle avganger for to påfølgende dager mellom 2 stasjoner
E - Registrer ny kunde
G - Finn og kjøp billetter
H - Finn din reisehistorikk\n
Q - Avslutte applikasjon\n''')

gyldige_valg = ['c', 'd', 'e', 'g', 'h','q']
valg = input('Hva vil du gjøre: (Skriv inn bokstav) ').lower()

while valg != 'q':
    while valg not in gyldige_valg:
        valg = input('Du må skrive inn en av bokstavene over: ').lower()


    if valg == 'c':
        historieC.main()
    elif valg == 'd':
        historieD.main()
    elif valg == 'e':
        historieE.main()
    elif valg == 'g':
        historieG.main()
    elif valg == 'h':
        historieH.main()
    else:
        break
    valg = input('''\nTjeneste utført! Hva vil du gjøre nå?\n
C - Søk etter ruter langs en bestemt stasjon
D - Finn alle avganger for to påfølgende dager mellom 2 stasjoner
E - Registrer ny kunde
G - Finn og kjøp billetter
H - Finn din reisehistorikk\n
Q - Avslutte applikasjon\n
Velg her: ''').lower()

print('\nTakk for at du brukte togdatabasen!\n')
print('Restart programmet (pil opp) for å bruke det igjen.')
