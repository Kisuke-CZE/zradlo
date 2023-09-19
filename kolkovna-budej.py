#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return  "https://budejovicka.kolkovna.cz/#poledni-menu"

def get_name():
    return "Kolkovna Budějovická"

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

    meme = soup.find("div", { "class": "op-menu-day active" })
    # print(meme)
    date = meme.find("h3").text
    matchzradlo = "^\s+([\w\d\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ„“\"\(\)\,\-\+]+) \|"
    matchcena = "^([0-9]+ Kč)"
    prevmatch = False
    nazev = ""
    cena = ""
    items = []
    for line in meme.text.splitlines():
      #print(line)
      zradlo = re.match(matchzradlo, line)
      if zradlo:
        nazev = zradlo.group(1).strip()
        prevmatch = True
      elif prevmatch:
        cenasub = re.match(matchcena, line)
        if cenasub:
          cena = cenasub.group(1).strip()
          items.append([nazev, cena])
        prevmatch = False
      else:
        prevmatch = False
        nazev = ""
      
    return(items, date)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)

        #date = return_date(bs)
        nazev = get_name()
        url = get_url()
        lokalita = "brumlovka"

        menu_list, date = return_menu(bs)

        return (nazev, url, date, menu_list, lokalita)
    except Exception as e:
        print(e)
        #return (get_name() + "- Chyba", "", str(e), [])
        nazev = get_name()
        url = get_url()
        lokalita = "brumlovka"
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    menu_list, date = return_menu(bs)
    print (date, menu_list)
