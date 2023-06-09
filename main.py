#nadanie poczatkowych zmiennych
warunki = ['saldo', 'sprzedaz', 'zakup', 'konto', 'lista', 'magazyn', 'przeglad', 'koniec']
stan_magazynu = dict()
historia_akcji = []
akcja = 0
stan_konta = 1000

#czesc pogramu odpowiadajaca za odczyt danych z pliku tekstowego i przypisywanie wartosci do zmiennych
filename = 'history.txt'
with open(filename, 'r') as f:
    for line in f:
        if 'Stan konta' in line:
            account, money = line.strip().split('&&')
            stan_konta = float(money)
        elif '%%' in line:
            k, v = line.strip().split('%%')
            stan_magazynu[k] = v
        elif '&&' in line:
            line = line.strip().replace('&&','')
            historia_akcji.append(line)

# wlasciwa czesc programu
while True :
# pytania w petli do uzytkownika
    print("1.Wpisz 'saldo' aby dodać lub odjąć kwotę z konta"  
          "\n2.Wpisz 'sprzedaz' aby wybrać SPRZEDAŻ"
          "\n3.Wpisz 'zakup' aby wybrać ZAKUP"
          "\n4.Wpisz 'konto' aby wyświetlić stan konta"
          "\n5.Wpisz 'lista' aby wyświetlić pełny stan magazynu"
          "\n6.Wpisz 'magazyn' aby wyświetlić ilość konkretnego produktu na stanie"
          "\n7.Wpisz 'przeglad' aby wyświetlić historię zmian"
          "\n8.Wpisz 'koniec' aby zakończyć działanie programu")
    zapytanie = input('Co wybierasz?: ')

# jezeli podanej wartosci nie ma na liscie warunkow program pyta uzytkownika jeszcze raz co chce zrobic
    if zapytanie not in warunki :
        print('Wpisałeś nieprawidłową wartość.Spróbuj jeszcze raz!')
        continue
# dodanie i odjecie przez uzytkownika kwoty z konta
    elif zapytanie == 'saldo':
        while True :
            zapytanie_o_saldo = int(input('Wybierz 1 jeżeli chcesz dodać kwotę. Wybierz 2 jeżeli chcesz odjąć kwotę: '))
            if zapytanie_o_saldo == 1 :
                saldo = float(input('Wpisz kwotę: '))
                stan_konta += saldo
                print(f'Dodano {saldo} $ do konta')
                akcja = f'Dodano {saldo} $ do konta'
                historia_akcji.append(akcja)
                break
            elif zapytanie_o_saldo == 2 :
                saldo = int(input('Wpisz kwotę: '))
                stan_konta -= saldo
                print(f'Odjęto {saldo} $ z konta')
                akcja = f'Odjęto {saldo} $ z konta'
                historia_akcji.append(akcja)
                break
            else :
                print('Podano nieprawidłową liczbę')

# sprzedaz, ktora dodaje kwote wpisana przez uzytkownika do salda i odejmuje dane produkty z magazynu
    elif zapytanie == 'sprzedaz' :
        nazwa_produktu = input('Podaj jaki produkt ma zostać sprzedany: ')
        if nazwa_produktu not in stan_magazynu:
            print('Nie ma takiego produktu w magazynie!')
        else:
            cena_produktu = float(input('Podaj cenę: '))
            liczba_sztuk = int(input('Podaj ilość: '))
            laczna_cena = cena_produktu * liczba_sztuk
            produkt_do_sprzedazy = stan_magazynu[nazwa_produktu]['ilość']
            if produkt_do_sprzedazy < liczba_sztuk:
                print('Nie ma takiej ilości!')
            else:
                produkt_do_sprzedazy -= liczba_sztuk
                stan_konta += laczna_cena
                stan_magazynu[nazwa_produktu]['ilość'] -= liczba_sztuk
                print(f'Sprzedano {nazwa_produktu} w ilości {liczba_sztuk} za {laczna_cena} $')
                akcja = f'Sprzedano {nazwa_produktu} w ilości {liczba_sztuk} za {laczna_cena} $'
                historia_akcji.append(akcja)

# zakup, ktory odejmuje kwote z konta i dodaje produkty do magazynu
    elif zapytanie == 'zakup' :
        nazwa_produktu = input('Podaj jaki produkt ma zostać zakupiony: ')
        if nazwa_produktu not in stan_magazynu:
            cena_produktu = float(input('Podaj cenę produktu: '))
            liczba_sztuk = int(input('Podaj liczbę zakupionych sztuk: '))
            laczna_cena = cena_produktu * liczba_sztuk
            if laczna_cena > stan_konta :
                print('Brakuje pieniędzy na zakup')
            elif laczna_cena < stan_konta :
                stan_magazynu[nazwa_produktu] = {'ilość': liczba_sztuk, 'cena': cena_produktu}
                stan_konta -= laczna_cena
                print(f'Zakupiono {nazwa_produktu} w ilości {liczba_sztuk} za {laczna_cena} $')
                akcja = f'Zakupiono {nazwa_produktu} w ilości {liczba_sztuk} za {laczna_cena} $'
                historia_akcji.append(akcja)
        else:
            print('Taki produkt znajduje się już na magazynie')

# podaje stan konta w $
    elif zapytanie == 'konto' :
        print(f'Stan konta to :{stan_konta} $')

# wyswietla wszystkie produkty ich ilosc i cene jakie sa w magazynie
    elif zapytanie == 'lista':
        print('Lista produktów w magazynie:')
        for k, v in stan_magazynu.items():
            print(f'{k} : {v}')

# wyswietla tylko jeden produkt podany przez uzytkownika
    elif zapytanie == 'magazyn':
        pytanie = input('Zapas jakiego produktu chcesz zobaczyć?: ')
        if pytanie not in stan_magazynu:
            print('Nie ma takiego produktu w magazynie!')
        else:
           print(f'{pytanie} : {stan_magazynu.get(pytanie)}')

# historia dokonanych przez uzytkownika akcji, ktore zapisuja sie na liscie
    elif zapytanie == 'przeglad' and len(historia_akcji) > 0:
        while True:
            while True:
                try:
                    liczba_od = int(input('Podaj początek zakresu: '))
                    liczba_do = int(input('Podaj koniec zakresu: '))
                    break
                except ValueError :
                    print(historia_akcji)
            if liczba_od <= 0 or liczba_do > len(historia_akcji) :
                print(f'Podałeś liczby spoza zakresu. Oto liczba dotychczasowych akcji : {len(historia_akcji)}')
            else :
                print(historia_akcji[liczba_od - 1 :liczba_do])
                break

# uzytkownik wpisujac koniec, konczy dzialanie programu
    elif zapytanie == 'koniec' :
# czesc kodu odpowiadajaca za zapisywanie wartosci do pliku tekstowego history.txt
        with open(filename, 'w') as f:
            f.write(f'Stan konta&&{stan_konta}\n')
        with open(filename, 'a') as f:
            for k, v in stan_magazynu.items():
                f.write(k + '%%')
                f.write(str(v) + '\n')
            for k in historia_akcji:
                f.write(k + '&&\n')
        break
