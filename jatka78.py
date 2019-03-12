#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    return "http://www.jatka78.cz/cs/bistro"

def get_name():
    return "Jatka 78"

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

    a = soup.find("table", { "class": "bistro-menu__items" }).find_all("tr", { "class": "bistro-menu__item" })
    #print(b)

    for item in a:
        #print(item)
        arr = []
        #print(item.text)
        if item.text.strip() != "":
          # print(item)
          nazev = item.find_all("td")[0].text.strip()
          cena = item.find_all("td")[1].text.strip()
          arr = [nazev, cena]
          items.append(arr)

    return items

def return_date(soup):
    b = soup.find("p", { "class": "bistro-menu__when-served" }).text.replace('\n', '')
    datum = re.sub(r'.*\/', ' ', b).strip()
    #print(datum)
    return(datum)

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
        url = get_url()
        lokalita = "holesovice"
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    date = return_date(bs)
    menu_list = return_menu(bs)
    # lol()

    #print(date, menu_list)
