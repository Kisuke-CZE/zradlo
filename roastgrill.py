#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
# from datetime import datetime
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "https://www.finegrill.cz/"

def get_name():
    return "Fine Grill Filadelfie"

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

    date = soup.find("div", { "class": "t-title_xxl" }).text
    if date is None:
      date = "???"
    items = []
    zradla = soup.find_all("div", {"class" : re.compile('.*pricelist-item__row.*')})
    for zradlo in zradla:
      #print(zradlo)
      nazev = zradlo.find("div", {"class" : re.compile('.*pricelist-item__title')})
      cena = zradlo.find("div", {"class" : re.compile('.*pricelist-item__price')})
      if ( nazev is None ) or ( cena is None ):
        continue
      items.append([nazev.text.strip(), cena.text.strip()])
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

    menu_list, date = return_menu(bs)
    print (date, menu_list)
