#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
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
    #print(soup)
    a = soup.find("div", { "class": "tmi-group mtop" }).find_all("div", { "class": "tmi tmi-daily pb5 pt5" })
    # print(a)

    for item in a:
      #print(item)
      #jidlo = item.find_all("div", { "class": "row" })[0].text.replace('\n', '').strip()
      nazev = item.find_all("div", { "class": "row" })[0].text
      #print(nazev)
      jidlo = re.sub(r'\n[\s]*', ' ', nazev).strip()
      cena = item.find_all("div", { "class": "row" })[1].text.strip()
      if cena:
        arr = []
        arr = [jidlo, cena]
        items.append(arr)

    return items

def return_date(soup):
    #b = ""
    b = soup.find("div", { "class": "tmi-group-name bold fontsize3 pb5 bb" }).text.strip()
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

    date = return_date(bs)
    menu_list = return_menu(bs)
    # lol()

    print(date, menu_list)
