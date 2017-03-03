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
        return soup

    else:
        return None

def return_menu(soup):
    a = soup.find("div", { "class": "dailyMenu" })
    #b = a.findNext("dm-day").text
    #c = b.findNext("p").text
    #d = re.split(" Kč", c)

    #date = soup.find("div", { "style": "background: rgba(34, 15, 15, .30); font-size: 20px; border-bottom: 1px solid #b7a56d;" }).text
    #date = soup.find_all("span", { "class":"datum" } )[0].text 
    date=""
    container = soup.find_all("table", {"class":"menu-table"})

    arr = []
    for i in range(0, len(container)):
        jidlo =  container[i].find_all("td")
        jidlo_obsah = jidlo[0]
        #jidlo_cena =   container[i].find_all("td", { "class":"menu-price" } )
        jidlo_cena = jidlo[1]
        arr.append([jidlo_obsah.text.replace("\t",""), jidlo_cena.text.replace("\t","")])
   
        
        # jidlo_cena.append(jidlo_obsah[i].findNext("td").text)
      #  arr.append([jidlo_obsah[i].text, jidlo_cena[i].text])
        
    items = arr


    print("ITEMS {0}".format(items))
    print("DATE", date)
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
    menu_list = return_menu(bs)
    print(menu_list)

    #debug_print(date, menu_list)
