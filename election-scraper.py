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
    url_data = projdi_odkazy_pridej_prefix(odkazy)
    volici_mesta_hl = projdi_jednotliva_mesta(url_data)
    hlasy_jednotlivych_stran = projdi_udaje_stran(url_data)
    df = pd.DataFrame({"Číslo obce": cisla_obce,
                       "Název obce": nazev_obce,
                       "Volící města": volici_mesta_hl,
                       "Strany": hlasy_jednotlivych_stran}
                      )
    df.to_csv('items.csv', encoding='utf-8')

def ziskej_parsovanou_odpoved(url: str):
    '''Získej rozdělenou odpověď na požadavek get.'''
    return bs4.BeautifulSoup(requests.get(url).text, features="html.parser")

def ziskej_informace_z_table(obsah):
    table = obsah.find("table", id="t%sa%")
    return table

def sloupec_cisla(data):
    '''Získej kódy všech obcí'''
    cisla = []
    for i in data.find_all("td", {"class": "cislo"}):
        cislo = i.text
        cisla.append(cislo)
    return cisla

def sloupec_nazev(data):
    '''Získej názvy všech obcí'''
    nazev = []
    for i in data.find_all("td", {"class": "overflow_name"}):
        obec = i.text
        nazev.append(obec)
    return nazev

def data_z_odkazu(data):
    '''Získej URL pro jednotlivé výsledky'''
    links = []
    for i in data.find_all("td", {"class": "cislo"}):
        for x in i.find_all("a"):
            links.append(x.get("href"))
    return links

def projdi_odkazy_pridej_prefix(url: list):
    for link in url:
        append_str = "https://volby.cz/pls/ps2017nss/"
        pre_res = [append_str + link for link in url]
    return pre_res

def projdi_jednotliva_mesta(url_mest):
    volici_mesta = []
    for url in url_mest:
        soup_mesta = ziskej_parsovanou_odpoved(url)
        volici = soup_mesta.find("table", {"class": "table"})
        volici_v_seznamu = volici.find_all("td", {"class": "cislo"})[3]. text.replace("\xa0", "")
        vydane_obalky = volici.find_all("td", {"class":"cislo"})[4].text.replace("\xa0", "")
        platne_hlasy = volici.find_all("td", {"class": "cislo"})[7].text.replace("\xa0", "")
        volici_mesta.append([volici_v_seznamu, vydane_obalky, platne_hlasy])
    return volici_mesta

def projdi_udaje_stran(url_mest):
    hlasy_stran = []
    for url in url_mest:
        soup_mesta = ziskej_parsovanou_odpoved(url)
        tabulka_hlasy = soup_mesta.find_all("div", {"class": "t2_470"})
        celkova_tabulka = []
        radky_tabulky = []
        celkem_hlasu_mesta = []

        for hlas in tabulka_hlasy:
            radky = hlas.find_all("tr")
            celkova_tabulka.extend(radky)

        for celek in celkova_tabulka:
            radek = celek.find_all("td", {"class": "cislo"})
            if radek:
                radky_tabulky.append(radek)
            else:
                continue

        for radek in radky_tabulky:
            celkem_hlasu_mesta.append(radek[1].text.replace("\xa0", ""))
        hlasy_stran.append(celkem_hlasu_mesta)

    return hlasy_stran

if __name__ == "__main__":
    main()
