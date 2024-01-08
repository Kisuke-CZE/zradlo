#!/usr/bin/env python3
# coding=utf-8

import requests, os, re, tempfile, time, locale
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "https://goodlunch.cz/kantyny/o2"

def get_content():
    page = requests.get(get_url())
    page.encoding = 'UTF-8'
    source = prepare_bs(page)
    url = source.find_all("link", { "as": "script" })[1]['href']
    # print(url)
    kantyna = requests.get(url)
    kantyna.encoding = 'UTF-8'
    # print(kantyna)
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    else:
        return "Error"

def get_name():
    return "Lunchbox Gamma"


def return_menu(soup):
    items = []
    date = soup.find("h2").text.strip()
    a = soup.find_all("li")

    for item in a:
      parts = item.find_all("p")
      nazev = parts[0].text.strip()
      cena = parts[2].text.strip(" [Kk]č").strip()
      if nazev and cena:
        arr = [nazev, str(cena) + " Kč"]
        items.append(arr)

    return (date, items)

def debug_print(date, menu):
    print(date)
    print(menu)

def result():
    lokalita = "brumlovka"
    try:
        #page = get_file()
        page = get_content()
        bs = prepare_bs(page)
        date, menu_list = return_menu(bs)
        nazev = get_name()
        url = get_url()


        return (nazev, url, date, menu_list, lokalita)
    except:
        #return(get_name() + " - Chyba", "", "Chyba", ["", "", ""])
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [], lokalita)

    os.remove(TMP)

if __name__ == "__main__":
    page = get_content()
    # print(page)
    bs = prepare_bs(page)
    # print(bs)
    date, menu_list = return_menu(bs)
    debug_print(date, menu_list)
    #print(result())
