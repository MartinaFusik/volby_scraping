"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Martina Fúsiková
email: martina.fusikova@gmail.com
discord: Martina_F#2319
"""

import requests
import bs4
import pandas as pd

def main():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
    odpoved = ziskej_parsovanou_odpoved(url)
    cisla_obce = sloupec_cisla(odpoved)
    nazev_obce = sloupec_nazev(odpoved)
    odkazy = data_z_odkazu(odpoved)
    df = pd.DataFrame({"Číslo obce": cisla_obce,
                       "Název obce": nazev_obce,
                       "Odkazy": odkazy}
                      )
    df.to_csv('items.csv', encoding='utf-8')

def ziskej_parsovanou_odpoved(url: str):
    '''Získej rozdělenou odpověď na požadavek get.'''
    return bs4.BeautifulSoup(requests.get(url).text, features="html.parser")

def ziskej_informace_z_table(obsah):
    table = obsah.find("table", id="t%sa%")
    return table

def sloupec_cisla(data):
    cisla = []
    for i in data.find_all("td", {"class": "cislo"}):
        cislo = i.text
        cisla.append(cislo)
    return cisla

def sloupec_nazev(data):
    nazev = []
    for i in data.find_all("td", {"class": "overflow_name"}):
        obec = i.text
        nazev.append(obec)
    return nazev

def data_z_odkazu(data):
    links = []
    for i in data.find_all("td", {"class": "cislo"}):
        for x in i.find_all("a"):
            links.append(x.get("href"))
    return links

if __name__ == "__main__":
    main()
