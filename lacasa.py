#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    return "https://www.lacasatrattoria.com/poledni-menu-1"

def get_name():
    return "La Casa Trattoria"

def get_file():
    kantyna = requests.get('https://menupraha.cz/restaurace/2833-la-casa-trattoria/')
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.content
        soup = BeautifulSoup(html.decode('utf-8', 'ignore'), 'html.parser')
        return soup

    else:
        return None

def return_menu(soup):
    a = soup.find_all("div", { "class": "panel panel-default" })[1]
    date = a.find("option").text.strip()
    dailymenu = a.find("tbody").find_all("tr")
    # print(dailymenu)
    items = []
    for item in dailymenu:
        # print("radek:",item.text)
        match = re.match("\s+([A-ZĚŠČŘŽÝÁÍÉÚŮŤŇÓÖ][A-Za-z0-9ěščřžýáíéůúťňóöŤĚŠČŘŽŇÝÁÍÉÚŮÓÖ ,\-–“\(\)]+)[\s\n]+([0-9]+ Kč)?\s+$", item.text)
        if match:
          nazev = match.group(1).strip()
          if match.group(2):
            cena = match.group(2).strip()
          else:
            cena = "Nestanovena"
          #print(nazev)
          #print(cena)
          items.append([nazev, cena])

    return(items, date)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)

        #date = return_date(bs)
        nazev = get_name()
        url = get_url()

        menu_list, date = return_menu(bs)

        return(nazev, url, date, menu_list)
    except Exception as e:
        print(e)
        #return (get_name() + "- Chyba", "", str(e), [])
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [])

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    # menu_list, date = return_menu(bs)
    # print(date, menu_list)

    #debug_print(date, menu_list)
