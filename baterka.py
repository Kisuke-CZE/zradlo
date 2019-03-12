#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    return "https://www.baterka.com/delnicka-holesovice"

def get_name():
    return "Baterka"

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
    items = []

    a = soup.find_all("table", { "class": "table" })
    b = soup.find_all("div", { "class": "sprocket-tabs-panel" })
    #print(b)

    for item in a[0].find_all("tr"):
        arr = []
        #print(item.text)
        if item.text.strip() != "":
          # print(item)
          nazev = item.find_all("td")[0].text.strip()
          cena = item.find_all("td")[1].text.strip()
          arr = [nazev, cena]
          items.append(arr)

    for item in b[0].find_all("p"):
      jidlo = item.text
      #print(jidlo)
      match = re.match("(.*)[\s]+([0-9]{2,3}[\s]*[KkČč\,\-]+)", jidlo)
      if match is not None:
          arr = []
          arr = [match.group(1).strip(), match.group(2).strip()]
      else:
          continue
      items.append(arr)

    return items

def return_date(soup):
    b = soup.find("div", { "class": "rt-block box5" }).find("div", { "class": "gantry-width-50 gantry-width-block" }).text.strip()
    #print(b)
    return(b)

def debug_print(date, menu):
    print(date)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"
        date = return_date(bs)
        menu_list = return_menu(bs)

        print(date, menu_list)
        return(nazev, url, date, menu_list, lokalita)
    except Exception as exp:
        print(exp)
        #return(get_name() + "- Chyba", "", "", [str(exp)])
        nazev = get_name()
        lokalita = "holesovice"
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    date = return_date(bs)
    menu_list = return_menu(bs)
    # lol()

    #print(date, menu_list)
