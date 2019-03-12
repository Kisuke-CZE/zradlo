#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from bs4 import BeautifulSoup

# locale.setlocale(locale.LC_ALL,'cs_CZ.UTF-8')
locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "http://www.restauracepetpenez.cz/"

def get_name():
    return "Pět peněz"

def get_file():
    kantyna = requests.get("http://www.restauracepetpenez.cz/homepage/poledni-menicka")
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.content
        soup = BeautifulSoup(html.decode('utf-8', 'ignore'), 'html.parser')
        return soup

    else:
        return None

def return_menu(soup):
    today = time.strftime("%A - %-d.%-m.%Y")
    # print(today)
    items = []
    published = False
    date = "???"
    a = soup.find_all("table")[0].find_all("tr")
    for item in a:
      # print(published)
      # print(str(item))
      line = item.find_all("td")
      try:
        day = line[0].strong.text.strip()
        #print(day)
        if day == today and not published:
          published = True
          date = day
          continue
        elif day != today and published:
          published = False
          continue
        else:
          published = False
      except Exception as NoneType:
        pass
      if published == True:
        nazev = line[2].text.strip()
        cena = line[3].text.strip()
        arr = [nazev, cena]
        items.append(arr)


    return(date, items)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)

        #date = return_date(bs)
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"

        date, menu_list = return_menu(bs)

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
    date, menu_list = return_menu(bs)
    print(date, menu_list)

    #debug_print(date, menu_list)
