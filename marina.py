#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    #return "http://www.manihi.cz/zavodni-stravovani-kantyna/kantyna-rosmarin-business-center/denni-menu"
    return "http://www.pivovarmarina.cz/menu/"

def get_name():
    return "Pivovar Marina"

def get_file():
    kantyna = requests.get(get_url())
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    else:
        return "Error"

def return_menu(soup):
    a = soup.find_all("div", { "class": "text_exposed_root text_exposed" })[0].find_all("p")
    date = a[0].text.strip()
    jidlo_pattern = '([0-9]. )?([\w\d\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ,]+)[\s]+([0-9]{2,3}[\s]*,-)'
    items = []

    for item in a:
        #print(item.text)
        match = re.match(jidlo_pattern, item.text)
        if match is not None:
          #print('match')
          jidlo = match.group(2).strip()
          cena = match.group(3).strip()
          arr = [jidlo, cena]
          items.append(arr)
        else:
          continue

    return items, date


def return_date(soup):
    b = soup.find_all("div", { "class": "text-content" })
    #print(b)
    b = b[1].find_all('h3')[0].text
    #b = b[0].h3.string
    b = b.replace("Denní nabídka ", "")
    return(b)

def debug_print(date, menu):
    print(date)
    print(menu)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"
        menu_list, date = return_menu(bs)

        #print(date, menu_list)
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

    #menu_list, date = return_menu(bs)
    #debug_print(date, menu_list)
