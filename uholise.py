#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    return "https://www.restu.cz/u-holise/denni-menu/"

def get_name():
    return "U Holiše"

def get_file():
    kantyna = requests.get(get_url())
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.content
        soup = BeautifulSoup(html.decode('utf-8', 'ignore'), 'html.parser')
        #print(soup)
        return soup

    else:
        return None

def return_menu(soup):
    a = soup.find("section", { "class": "restaurant-menu-list" })
    arr = []
    try:
        date = a.find("h4").text
        menicko = a.find("ul", {"class":"c-menu-content"}).find_all("li", {"class":"c-menu-item"})
        #print(menicko)
        for item in menicko:
            jidlo =  item.find_all("li")
            jidlo_obsah = jidlo[0]
            jidlo_cena = jidlo[1]
            arr.append([jidlo_obsah.text.replace("\t",""), jidlo_cena.text.replace("\t","")])

    except:
        menicko = soup.find_all("table", { "class": "menu-table" })
        date = menicko[0].find("h3").text
        #print(menicko)
        for item in menicko:
            jidlo =  item.find_all("td")
            jidlo_obsah = jidlo[0]
            jidlo_cena = jidlo[1]
            arr.append([jidlo_obsah.text.replace("\t","").strip(), jidlo_cena.text.replace("\t","").strip()])

    items = arr

    return(items, date)

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
        return (get_name() + "- Chyba", "", str(e), [])

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    #menu_list, date = return_menu(bs)
    #print(date, menu_list)

    #debug_print(date, menu_list)
