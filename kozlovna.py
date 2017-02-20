#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    return "http://www.holesovickakozlovna.cz/"

def get_name():
    return "Holešovická Kozlovna"

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
    a = soup.find("div", { "class": "dailyMenu" })
    #b = a.findNext("dm-day").text
    #c = b.findNext("p").text
    #d = re.split(" Kč", c)

    date = soup.find("div", { "class": "dm-day" }).text.replace("Polední nabídka", "")
    jidlo_obsah = soup.find_all("span", { "class": "td-jidlo-obsah"} )
    jidlo_cena =  soup.find_all("td", { "class": "td-cena"} )
    arr = []
    for i in range(0, len(jidlo_obsah)):
        arr.append([jidlo_obsah[i].text, jidlo_cena[i].text])


    items = arr


    print("ITEMS {0}".format(items))
    print("DATE", date)
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
        return (get_name() + "- Chyba", "", str(e), [])

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    menu_list = return_menu(bs)

    #debug_print(date, menu_list)
