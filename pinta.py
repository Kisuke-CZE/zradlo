#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "http://www.pinta-restaurace.cz/denni_menu.php"

def get_name():
    return "Pinta"

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
    a = soup.find("div", { "class": "dailyMenu" })

    jidlo_obsah =  soup.find_all("tr" )

    jidlo_cena = []
    items = []
    today = time.strftime("%A %d.%m.%Y")
    #print(today)
    published = False
    date = "???"
    for i in jidlo_obsah:
        if i.text != "":
          # print (i)
          if i.text.strip() == "Nápoj:" and published:
              break

          if published:
              zradlo = i.find_all("td")
              #print(zradlo)
              nazev = zradlo[1].text
              cena = zradlo[2].text
              #print(cena)
              #print(nazev)
              arr = [nazev, cena]
              items.append(arr)

          if i.text.strip() == today and not published:
              published = True
              date = today

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
    # menu_list, date = return_menu(bs)
    # print(date, menu_list)
