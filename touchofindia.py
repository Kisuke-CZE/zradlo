#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from bs4 import BeautifulSoup


def get_url():
    return "https://touchofindia.cz/daily-lunch-menu"

def get_name():
    return "Touch of India"

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
    locale.setlocale(locale.LC_ALL,'en_US.utf8')
    today = time.strftime(".*%-d(st|nd|rd|th)\s+%B.*$").lower()
    locale.setlocale(locale.LC_ALL,'')
    #print(today)
    items = []
    date = "???"
    a = soup.find_all("div", {"class": "menu-category"})
    #print(a)
    for menu in a:
        preddatum = menu.findChildren()[1]
        #print(preddatum.text)
        match = re.match(today, preddatum.text.lower())
        if match:
            date = re.match('.*\(([\w\'\s]+)\).*$', preddatum.text).group(1)
            #print(menu)
            b = menu.find("div", {"data-ux": "Block"}).findChildren("div", {"data-ux": "Block"}, recursive=False)
            for item in b:
                #print(item)
                nazev = item.find("div", {"data-ux": "Grid"}).text.replace('\xa0','').strip()
                cena = item.find("div", {"data-ux": "Block"}).p.text.strip()
                if nazev and cena:
                    arr = [nazev, cena]
                    items.append(arr)
    return(date, items)

def result():
    lokalita = "brumlovka"
    try:
        file = get_file()

        bs = prepare_bs(file)

        #date = return_date(bs)
        nazev = get_name()
        url = get_url()

        date, menu_list = return_menu(bs)

        return(nazev, url, date, menu_list, lokalita)
    except Exception as e:
        print(e)
        #return (get_name() + "- Chyba", "", str(e), [])
        nazev = get_name()
        url = get_url()

        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    date, menu_list = return_menu(bs)
    print(date, menu_list)

    #debug_print(date, menu_list)
