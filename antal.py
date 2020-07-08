#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from bs4 import BeautifulSoup

def get_url():
    return "https://www.restauraceantal.cz/aktualne"

def get_name():
    return "Antal"

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
    date = "???"
    items = []
    locale.setlocale(locale.LC_ALL,'cs_CZ.UTF-8')
    today = time.strftime("%A %-d.%-m.%Y")
    #print(today)
    a = soup.find_all("div", { "class": "title-box" })
    #print(a)
    for item in a:
        nazev = item.find("h3").text.strip()
        cena = item.find("span", { "class": "price" }).text.strip('Kč ')
        if nazev and int(cena) > 1:
            items.append([nazev, cena + ' Kč'])

    if items:
        date = today
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
