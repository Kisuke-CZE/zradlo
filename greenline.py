#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from bs4 import BeautifulSoup

# locale.setlocale(locale.LC_ALL,'cs_CZ.UTF-8')
locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "http://www.cateringmelodie.cz/lunch-garden-denni-menu-green_line"

def get_name():
    return "Lunch Garden Greenline"

def get_file():
    kantyna = requests.get("http://www.cateringmelodie.cz/lunch-garden-denni-menu-green_line")
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.content
        soup = BeautifulSoup(html.decode('utf-8', 'ignore'), 'html.parser')
        return soup

    else:
        return None

def return_menu(soup):
    today = time.strftime("%A").lower()
    items = []
    published = False
    date = "???"
    a = soup.find("div", {"class": "daily-menu"}).findChildren()
    for item in a:
      if item.name == 'h3' and item.text.strip() == today:
        date = item.text.strip()
        published = True
      elif item.name == 'h3' and published:
        published = False
        break
      if published == True and item.name == 'p':
        nazev = item.text.strip()
        cena = ''
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
    #date, menu_list = return_menu(bs)
    #print(date, menu_list)

    #debug_print(date, menu_list)
