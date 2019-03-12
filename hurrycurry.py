#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "http://hurrycurry.cz/na-maninach/"

def get_name():
    return "Hurry Curry"

def get_today_url():
    today = time.strftime("%A")
    # print(today)
    menumap = {
      'Pondělí': "http://hurrycurry.cz/na-maninach/index.php?route=product/category&path=97_98",
      'Úterý': "http://hurrycurry.cz/na-maninach/index.php?route=product/category&path=97_99",
      'Středa': "http://hurrycurry.cz/na-maninach/index.php?route=product/category&path=97_100",
      'Čtvrtek': "http://hurrycurry.cz/na-maninach/index.php?route=product/category&path=97_101",
      'Pátek': "http://hurrycurry.cz/na-maninach/index.php?route=product/category&path=97_102",
    }
    return menumap.get(today, "Hovno")

def get_file():
    kantyna = requests.get(get_today_url())
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.content
        soup = BeautifulSoup(html.decode('utf-8', 'ignore'), 'html.parser')
        return soup

    else:
        return None

def return_menu(soup):
    #print(soup)
    items = []
    date = time.strftime("%A")
    jidla = soup.find_all("div", { "class": "product-details" })
    for jidlo in jidla:
        nazev = jidlo.find("p", { "class": "description"}).text.strip()
        cena_text = jidlo.find("p", { "class": "price"}).text.strip()
        match = re.match('([0-9\,]{2,6}\s+Kč)\s+.*', cena_text)
        if match is not None:
            cena = match.group(1)
        else:
            continue
        arr = [nazev, cena]
        #print(arr)
        items.append(arr)
    return(items, date)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)

        #date = return_date(bs)
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"

        menu_list, date = return_menu(bs)

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
    # date = 'Dneska'
    #menu_list, date = return_menu(bs)
    #print(date, menu_list)

    #debug_print(date, menu_list)
