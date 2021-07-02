#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    return "https://baterka.com/#menu"

def get_name():
    return "Baterka"

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
    items = []

    a = soup.find("div", { "class": "tab-content1" }).find("div", { "class": "tab active" }).find_all("div", { "class": "df-spl-row name-price" })

    for item in a:
        nazev = item.find("div", { "class": "name a-tag" }).text.strip()
        cena = item.find("div", { "class": "spl-price a-tag" }).text.strip()
        #print(nazev + ": " + cena)
        if nazev and cena:
          items.append([nazev, cena])

    return items

def return_date(soup):
    b = soup.find("div", { "class": "custom-description-section" }).find_all(text=True)[0].strip()
    #print(b)
    return(b)

def debug_print(date, menu):
    print(date)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"
        date = return_date(bs)
        menu_list = return_menu(bs)

        print(date, menu_list)
        return(nazev, url, date, menu_list, lokalita)
    except Exception as exp:
        print(exp)
        #return(get_name() + "- Chyba", "", "", [str(exp)])
        nazev = get_name()
        lokalita = "holesovice"
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    date = return_date(bs)
    menu_list = return_menu(bs)
    # lol()

    print(date, menu_list)
