# volby_scraping
Třetí projekt do Engeto Python online akademie.

# Popis projektu
Projekt slouží k extrahování výsledků parlamentních voleb z roku 2017. Odkaz k prohlédnutí naleznete <a href="https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ">zde</a>.

# Instalace knihoven
Knihovny, které jsou použity v kódu jsou uložené v souboru requirements.txt. Pro instalaci doporučuji vytvořit nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:

```
$ pip3 --verison                    # ověření verze manageru
$ pip3 install -r requirements.txt  # nainstalování knihoven
```
# Spouštení projektu
Spuštění souboru election-scraper.py v rámci příkazového řádku požaduje dva povinné argumenty.

```
python election-scraper.py "url_uzemniho_celku" "vysledny_soubor.csv"
```

Následně se vám stáhnou výsledky jako soubor s příponou ```.csv.```

# Ukázka projektu
Ukázka projektu pro okres Prostějov:

1. argument https://volby.cz/pls/ps2017/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
2. argument prostejov.csv

## Spuštění programu:
```
python election-scraper.py "https://volby.cz/pls/ps2017/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "prostejov.csv"
```

## Průběh stahování:
```
Stahuji data z url: https://volby.cz/pls/ps2017/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
Ukládám data do souboru: prostejov.csv
Ukoncuji election-scraper.py
```

## Částečný výstup:
```
Číslo obce,Název obce,Voliči v seznamu,Vydané obálky,...
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
589276,Bílovice-Lutotín,431,279,275,13,0,0,32,0,8,40,1,0,4,0,0,30,0,3,83,0,0,22,0,0,0,1,38,0
589284,Biskupice,238,132,131,14,0,0,9,0,5,24,2,1,1,0,0,10,2,0,34,0,0,10,0,0,0,0,19,0
...
```
