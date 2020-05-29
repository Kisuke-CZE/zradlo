#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from datetime import datetime
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL,'')

def get_url():
    base_url = "http://gth.cz"
    menu_url = "/provoz/bbc-beta/jidelni-listek"
    main_menu = requests.get(base_url+menu_url)
    if main_menu is not None and main_menu.status_code == 200:
        today = time.strftime("%A %-d.%-m.%Y")
        html = main_menu.text
        soup = BeautifulSoup(html, 'html.parser')
        dny = soup.find_all("a", { "class": "btn btn-default noTextDec" })
        # print(dny)
        # print(today)
        for den in dny:
            if today in den.text:
                link = base_url+den['href']
                break
        if link is not None:
            return link
        else:
            return "Error"
    else:
        return "Error"

def get_name():
    return "GTH Beta"

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

    a = soup.find("div", { "class": "day_wrapper" })
    date = a.h4.text
    b = a.find_all("div", { "class": "meat_wrapper" })
    items = []
    for item in b:
        # print(item)
        grid = item.find_all("div", { "class": "col-xs-8" })
        jidlo = grid[0].text.strip()
        cena = grid[2].text.strip()
        if jidlo is not None and cena is not None:
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

    menu_list, date = return_menu(bs)
    print (date, menu_list)
