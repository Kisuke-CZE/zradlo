#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, locale
from bs4 import BeautifulSoup

def get_url():
    return "http://restauracepragos.cz/menu/poledni-menu/"

def get_name():
    return "Pragos"

def get_file():
    user_agent = {'User-agent': 'Mozilla/5.0'}
    kantyna = requests.get(get_url(), headers = user_agent)
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
    date = soup.find("div", { "class": "znColumnElement-innerContent" }).find("h1", { "class": "dn-heading" }).text.strip("DENNÍ MENU").strip()
    # print(date)
    a = soup.find_all("div", { "class": "priceListElement-itemRight" })

    for item in a:
      nazev = item.find("h4", { "class": "priceListElement-itemTitle" }).text.strip()
      cena = item.find("div", { "class": "priceListElement-itemPrice" }).text.strip()
      items.append([nazev, cena])

    return date, items

def debug_print(date, menu):
    print(date)

def result():
    lokalita = "brumlovka"
    try:
        file = get_file()

        bs = prepare_bs(file)
        nazev = get_name()
        url = get_url()
        date, menu_list = return_menu(bs)

        #print(date, menu_list)
        return(nazev, url, date, menu_list, lokalita)
    except Exception as exp:
        print(exp)
        #return(get_name() + "- Chyba", "", "", [str(exp)])
        nazev = get_name()
        usrl = get_url()
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    date, menu_list = return_menu(bs)
    # lol()

    print(date, menu_list)
