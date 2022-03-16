#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from bs4 import BeautifulSoup

def get_url():
    return "https://www.zomato.com/cs/praha/restaurace-alfa-michle-praha-4/denní-menu"

def get_name():
    return "Alfa"

def get_file():
    user_agent = {'User-agent': 'Mozilla/5.0'}
    kantyna = requests.get("https://www.zomato.com/cs/praha/restaurace-alfa-michle-praha-4/denní-menu", headers = user_agent)
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
    date = "???"
    locale.setlocale(locale.LC_ALL,'cs_CZ.UTF-8')
    today = time.strftime("%A %-d.%-m.%Y")
    a = soup.main.div.find_all("section", recursive=False)[3].div.find_all("div", recursive=False)[1]

    for item in a:
      # print(item)
      if item.find("div"):
        jidlo = item.div.find_all("div")
        if jidlo:
          nazev = jidlo[0].text
          cena = jidlo[1].text.strip(' Kč').replace('\xa0','')
          if re.match("\s*[0-9]+\s*", cena):
            items.append([nazev, cena + ' Kč'])

    if items:
      date = today
    return(items, date)

def debug_print(date, menu):
    print(date)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)
        nazev = get_name()
        url = get_url()
        lokalita = "brumlovka"
        date = return_date(bs)
        menu_list = return_menu(bs)

        print(date, menu_list)
        return(nazev, url, date, menu_list, lokalita)
    except Exception as exp:
        print(exp)
        #return(get_name() + "- Chyba", "", "", [str(exp)])
        nazev = get_name()
        url = get_url()
        lokalita = "brumlovka"
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    #menu_list = return_menu(bs)
    menu_list, date = return_menu(bs)

    print(date, menu_list)
