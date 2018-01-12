#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    return "http://www.restaurantport58.cz/denni-nabidka/"

def get_name():
    return "Port 58"

def get_file():
    user_agent = {'User-agent': 'Mozilla/5.0'}
    kantyna = requests.get(get_url())
    # kantyna.encoding = 'UTF-8'
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.text
        #print(html)
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    else:
        return "Error"

def return_menu(soup):
    items = []
    a = soup.find("div", { "class": "column central" }).find_all("li")
    #print(a)

    for item in a:
      if item.text.strip():
          nazev = item.find("p", { "class": "item-text" }).text.strip()
          b = item.find_all("div", { "class": "value-col" })
          cena = ""
          for price in b:
              if price.text.strip():
                  cena = price.text.strip()
          # print(nazev, cena)
          arr = [nazev, cena]
          items.append(arr)

    return items

def return_date(soup):
    b = soup.find("h3", { "class": "jsrm-menu-header" }).text.strip()
    match = re.match(".*\s([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4})", b)
    date = match.group(1).strip()
    #print(b)
    return(date)

def debug_print(date, menu):
    print(date)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)
        nazev = get_name()
        url = get_url()
        date = return_date(bs)
        menu_list = return_menu(bs)

        print(date, menu_list)
        return(nazev, url, date, menu_list)
    except Exception as exp:
        print(exp)
        #return(get_name() + "- Chyba", "", "", [str(exp)])
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [])

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    #menu_list = return_menu(bs)
    # lol()

    #print(date, menu_list)
