#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    return "https://www.motoburger.cz/"

def get_name():
    return "Motoburger"

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

def return_menu(soup):
    a = soup.find_all("tr")
    # print(a)
    items = []
    date = "???"
    for item in a:
      try:
        nazev = item.find_all("td")[0].find_all("a")[0].text.strip()
        cena = item.find_all("td")[1].text.strip()
        if nazev and cena and ( nazev != "ROZVOZ PO HOLEŠOVICÍCH ZDARMA" and not re.match('Objednávky s sebou na tel.*', nazev) ):
          arr = [nazev, cena]
          items.append(arr)
      except Exception as IndexError:
        continue

    return (items)

def return_date(soup):
    a = soup.find_all("td")[0].text
    return(a)

def debug_print(date, menu):
    print(date)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"
        menu_list = return_menu(bs)
        date = return_date(bs)

        print(date, menu_list)
        return(nazev, url, date, menu_list, lokalita)
    except Exception as exp:
        print(exp)
        #return(get_name() + "- Chyba", "", "", [str(exp)])
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    date = return_date(bs)
    menu_list = return_menu(bs)

    #print(date, menu_list)
