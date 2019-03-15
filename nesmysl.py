#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "https://www.restaurantnesmysl.cz/denni-nabidka"

def get_name():
    return "ne-SMYSL"

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
    date = soup.find("div", { "class": "row p-4 border-bottom"}).find("span", {"class": "pl-2"}).text
    a = soup.find("div", { "class": "container mt-4 mb-4" }).find_all("div", { "class": "row"})
    items = []
    for item in a:
      #print(item)
      jidlo = item.find("div", { "class": "col-md-8" }).text.strip()
      cena = item.find("div", { "class": "col-md-4 text-right" }).text.replace('Kč','').strip()
      if jidlo and cena:
          arr = [jidlo, cena]
          items.append(arr)

    return(items, date)


def result():
    lokalita = "brumlovka"
    try:
        file = get_file()

        bs = prepare_bs(file)

        nazev = get_name()
        url = get_url()

        menu_list, date = return_menu(bs)

        return (nazev, url, date, menu_list, lokalita)
    except Exception as e:
        print(e)
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    menu_list, date = return_menu(bs)
    print (date, menu_list)
