#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from bs4 import BeautifulSoup

# locale.setlocale(locale.LC_ALL,'cs_CZ.UTF-8')
locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "https://phillscorner.cz/"

def get_name():
    return "Phill’s Corner"

def get_file():
    kantyna = requests.get(get_url())
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.content
        soup = BeautifulSoup(html.decode('utf-8', 'ignore'), 'html.parser')
        return soup

    else:
        return None

def return_menu(soup):
    today = time.strftime("%A")
    #print(today)
    items = []
    published = False
    date = "???"
    jidelak = soup.find_all("div", { "class": "menu-line" })
    #print(days)
    for jidlo in jidelak:
      #print(jidlo)
      nazev = jidlo.find("span", { "class": "title" }).text.split('(')[0].strip()
      cena = jidlo.find("span", { "class": "price" }).text
      items.append([nazev, cena])
    #print(date)


    return(date, items)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)

        #date = return_date(bs)
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"

        date, menu_list = return_menu(bs)

        return(nazev, url, date, menu_list, lokalita)
    except Exception as e:
        print(e)
        #return (get_name() + "- Chyba", "", str(e), [])
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    date, menu_list = return_menu(bs)
    print(date, menu_list)

    #debug_print(date, menu_list)
