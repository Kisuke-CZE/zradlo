#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "http://www.melina.cz/michelska/"

def get_name():
    return "Melina Michelská"

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
    a = soup.find("div", {"id": "restaurant-menu-daily"})
    #print(a)
    date = a.find("h1", {"class": "text-center"}).text.replace('Denní menu', '').strip()
    b = a.find_all("div", {"class": "menu-item"})
    items = []
    for item in b:
        #print(item)
        jidlo = item.find("div", {"class": "menu-item-name"}).text.strip()
        cena  = item.find("div", {"class": "menu-item-price"}).text.strip()
        if jidlo and cena:
            arr = [jidlo, cena]
            items.append(arr)
        else:
            continue
    return(items, date)


def result():
    try:
        file = get_file()

        bs = prepare_bs(file)

        nazev = get_name()
        url = get_url()
        lokalita = "brumlovka"

        menu_list, date = return_menu(bs)

        return (nazev, url, date, menu_list, lokalita)
    except Exception as e:
        print(e)
        nazev = get_name()
        url = get_url()
        lokalita = "brumlovka"
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #menu_list, date = return_menu(bs)
    #print (date, menu_list)
