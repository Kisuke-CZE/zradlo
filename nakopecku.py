#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "https://www.restaurace-nakopecku.cz/"

def get_name():
    return "Na kopečku"

def get_file():
    kantyna = requests.get(get_url())
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    else:
        return "Error"

def return_menu(soup):
    items = []
    meme = soup.find("div", { "class": "dailyMenu" })
    # print(meme)
    day = meme.find("div", { "class": "dm-day"}).text
    date = re.match(("\s*Polední nabídka (.*)"), day).group(1)
    zradla = meme.find_all("tr")
    for zradlo in zradla:
        # print(zradlo)
        gramaz = zradlo.find("td", { "class": "td-cislo" })
        nazev = zradlo.find("td", { "class": "td-popis" })
        cena = zradlo.find("td", { "class": "td-cena" })
        if nazev:
          gramaz = gramaz.text
          nazev = nazev.text
          cena = cena.text
          if gramaz and cena:
            #print(nazev)
            items.append([nazev,cena])

    return(date, items)


#def return_date(soup):
#	return("")

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)

        #date = return_date(bs)
        nazev = get_name()
        url = get_url()
        lokalita = "brumlovka"

        menu_list, date = return_menu(bs)

        return (nazev, url, date, menu_list, lokalita)
    except Exception as e:
        print(e)
        #return (get_name() + "- Chyba", "", str(e), [])
        nazev = get_name()
        url = get_url()
        lokalita = "brumlovka"
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    date, menu_list = return_menu(bs)
    print(date)
    print(menu_list)

    #debug_print(date, menu_list)
