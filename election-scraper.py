"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Martina Fúsiková
email: martina.fusikova@gmail.com
discord: Martina_F#2319
"""

import requests
import bs4
import pandas as pd
import sys

def main():
    if len(sys.argv) != 3:
        print("Pro spuštění zapiš argumenty v následujícím tvaru:",
              "election-scraper.py 'URL' 'nazev_souboru.csv'",
              sep="\n")
    elif "volby.cz/pls/ps2017nss/" not in sys.argv[1]:
        print("Špatně zadaná webová adresa okresu!")
    elif ".csv" not in sys.argv[2]:
        print("Název souboru musí končit '.csv' (např. 'vysledky.csv')")
    else:
        zapis_do_csv(sys.argv[1], sys.argv[2])
    print("Ukončuji elections_scraper.py")

def ziskej_parsovanou_odpoved(url):
    '''Získej rozdělenou odpověď na požadavek get.'''
    return bs4.BeautifulSoup(requests.get(url).text, features="html.parser")

def najdi_mesta(url):
    soup = ziskej_parsovanou_odpoved(url)
    mesta = soup.find_all("tr")
    return mesta

def najdi_udaje_mesta(url):
    mesta = najdi_mesta(url)
    udaje_mesta = []
    for mesto in mesta:
        nazev_mesta = mesto.find("td", {"class": "overflow_name"})
        kod_mesta = mesto.find("td", {"class": "cislo"})
        if nazev_mesta:
            udaje_mesta.append([kod_mesta.text, nazev_mesta.text])
        else:
            continue
    return udaje_mesta

def data_z_odkazu(data):
    '''Získej URL pro jednotlivé výsledky'''
    links = []
    for i in data.find_all("td", {"class": "cislo"}):
        for x in i.find_all("a"):
            links.append(x.get("href"))
    return links

def projdi_odkazy_pridej_prefix(url):
    '''Přidá prefix ke každé relativní url'''
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

def projdi_nazvy_stran(url_mest):
    nazvy_stran = []
    soup_strany = ziskej_parsovanou_odpoved(url_mest)
    tabulka_nazvy = soup_strany.find_all("td", {"class": "overflow_name"})
    for nazev in tabulka_nazvy:
        nazvy_stran.append(nazev.text)
    return nazvy_stran

def vytvor_hlavicku_tabulky(url):
    url_mesta = projdi_odkazy_pridej_prefix(url)[0]
    hlavicka_tabulky = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné Hlasy"]
    nazvy_stran = projdi_nazvy_stran(url_mesta)
    hlavicka_tabulky.extend(nazvy_stran)
    return hlavicka_tabulky

def vytvor_vysledky_obce(url):
    url_mest = projdi_odkazy_pridej_prefix(url)
    vysledky_obce = najdi_udaje_mesta(url)
    volici_mesta = projdi_jednotliva_mesta(url_mest)
    vysledky_stran = projdi_udaje_stran(url_mest)
    for i in range(len(vysledky_obce)):
        vysledky_obce[i].extend(volici_mesta[i])
    for j in range(len(vysledky_obce)):
        vysledky_obce[j].extend(vysledky_stran[j])
    return vysledky_obce

def zapis_do_csv(url, nazev_souboru):
    print(f"STAHUJI DATA Z VYBRANEHO URL: {url}")
    vysledky_obce = vytvor_vysledky_obce(url)
    hlavicka_tabulky = vytvor_hlavicku_tabulky(url)
    print(f"UKLADAM DO SOUBORU: {nazev_souboru}")
    df = pd.DataFrame(hlavicka_tabulky, vysledky_obce)
    df.to_csv(nazev_souboru, encoding='utf-8')

if __name__ == "__main__":
    main()
