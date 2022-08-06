"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Martina Fúsiková
email: martina.fusikova@gmail.com
discord: Martina_F#2319
"""
import bs4
import csv
import requests
import pandas as pd

def main():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103"
    odpoved = ziskej_parsovanou_odpoved(url)
    zahlavi, zdroj = rozdel_zahlavi_a_data(vyber_jen_tr_tagy(odpoved))
    final_radek = rozdeleni_zdroje(zdroj)
    print(zahlavi, final_radek)
def ziskej_parsovanou_odpoved(url: str):
    '''Získej rozdělenou odpověď na požadavek get.'''
    return bs4.BeautifulSoup(requests.get(url).text, features="html.parser")

def vyber_jen_tr_tagy(soup: bs4.BeautifulSoup) -> bs4.element.ResultSet:
    '''Ze zdrojového kódu vybere všechny tagy "tr"'''
    return soup.findAll("tr")

def rozdel_zahlavi_a_data(all_tr: bs4.element.ResultSet):
    header_tag, *data = all_tr[1:]
    header: list = header_tag.get_text().splitlines()[1:]
    return header, data

def rozdeleni_zdroje(obsah: bs4.element.ResultSet):
    headers, *others = obsah
    data: list = headers.get_text().splitlines()[1:3]
    return data

if __name__ == "__main__":
    main()