#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    return "http://avion58.cz/"

def get_name():
    return "Avion58"

def get_file():
    kantyna = requests.get(get_url())
    kantyna.encoding = 'UTF-8'
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    else:
        return "Error"

def return_date(soup):
    b = soup.find("div", { "class": "levy-sloupec denni-menu" }).find("div", { "class": "box" }).span.text.strip()
    return(b)

def return_menu(soup):
    items = []
    datum = "???"

    b = soup.find("div", { "class": "levy-sloupec denni-menu" }).find("div", { "class": "box" }).text
    # print(b)
    for item in b.splitlines():
      if item != "":
        # print(item)
        match = re.match("^(Polévky|Hlavní jídla|Saláty|Naše limonády|Dezerty)?([A-ZĚŠČŘŽÝÁÍÉÚŮŤŇ][A-Za-zěščřžýáíéůúťňŤĚŠČŘŽŇÝÁÍÉÚŮ \,\-\–“\n\r\t]+)([0-9]+,-)$", item)
        if match is not None:
          arr = []
          nazev = match.group(2).strip()
          cena = match.group(3).strip()
          items.append([nazev, cena])
          # print(nazev)
        else:
          continue
      else:
        continue

    return items


def debug_print(date, menu):
    print(date)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)
        nazev = get_name()
        url = get_url()
        date = return_date(bs)
        menu_list = return_menu(bs)

        print(date, menu_list)
        return(nazev, url, date, menu_list)
    except Exception as exp:
        print(exp)
        #return(get_name() + "- Chyba", "", "", [str(exp)])
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [])

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    #menu_list = return_menu(bs)

    #print(date, menu_list)
