#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    return "http://avion58.cz/"

def get_name():
    return "Avion58"

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

    b = soup.find_all("div", { "class": "jidlo" })
    for item in b:
      arr = []
      #jidlo = BeautifulSoup(str(item), 'html.parser')
      # arr = [jidlo.find("strong").text, jidlo.find("strong", { "class": "price" }).text]
      nazev = item.find("strong").text
      if nazev == "":
        # print(item.text)
        match = re.match("\s+([A-ZĚŠČŘŽÝÁÍÉÚŮŤŇ][A-Za-zěščřžýáíéůúťňŤĚŠČŘŽŇÝÁÍÉÚŮ \,\-\–“\n\r\t]+)", item.text)
        if match is not None:
          nazev = match.group(1).strip()
        else:
          continue
        # nazev = item.text
      cena = item.find("strong", { "class": "price" }).text
      arr = [nazev, cena]
      # match = re.match("(.*?)([0-9]{2,3}\,\-)", item)
      items.append(arr)

    return items


def return_date(soup):
    b = soup.find("div", { "class": "datum" }).text
    #print(b)
    #b = b[1].find_all('h3')[0].text
    #b = b[0].h3.string
    #b = b.replace("Denní nabídka ", "")
    return(b)

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
