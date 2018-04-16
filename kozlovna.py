#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    return "http://www.holesovickakozlovna.cz/"

def get_name():
    return "Holešovická Kozlovna"

def get_file():
    kantyna = requests.get(get_url(), timeout=2)
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    else:
        return "Error"

def return_menu(soup):
    a = soup.find("div", { "class": "dailyMenu" })
    #b = a.findNext("dm-day").text
    #c = b.findNext("p").text
    #d = re.split(" Kč", c)

    date = soup.find("div", { "class": "dm-day" }).text.replace("Polední nabídka", "").strip()
    jidelak =  soup.find_all("tr")
    arr = []
    for item in jidelak:
      nazev = item.find("td", { "class": "td-popis" })
      cena = item.find("td", { "class": "td-cena" })
      objem = item.find("td", { "class": "td-cislo" })
      if cena and cena.text:
          jidlo_nazev = nazev.text.strip()
          jidlo_cena = cena.text.strip()
          jidlo_objem = objem.text.strip()
          if jidlo_objem:
            jidlo_nazev = jidlo_nazev + ' ' + jidlo_objem
          arr.append([jidlo_nazev, jidlo_cena])

    items = arr
    return(items, date)


#def return_date(soup):
#	return("")

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)

        #date = return_date(bs)
        nazev = get_name()
        url = get_url()

        menu_list, date = return_menu(bs)

        return(nazev, url, date, menu_list)
    except Exception as e:
        print(e)
        #return (get_name() + "- Chyba", "", str(e), [])
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [])

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    menu_list, date = return_menu(bs)

    #print(date)
    #print(menu_list)
