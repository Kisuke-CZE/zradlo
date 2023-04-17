#!/usr/bin/env python3
# coding=utf-8
# VRTULE

import requests, os, re, tempfile, time, locale

from bs4 import BeautifulSoup
from subprocess import check_output

locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "https://www.cantina-lafresca.cz/menu/brumlovka"

def get_content():
    print("Stahuji menu")
    kantyna = requests.get(get_url())
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.content
        soup = BeautifulSoup(html.decode('utf-8', 'ignore'), 'html.parser')
        return soup
    
def get_name():
    return "La Fresca Filadelfie"

def return_menu(soup):
    # datum
    today = time.strftime("%A %d. %-m. %Y").lower()
    #print(today)
    items = []
    date = ''
    column = 0
    table = soup.find("div", {"class": "table-responsive"}).find_all("tr")
    #print(table[0])
    days = table[0].find_all("th")
    for idx, day in enumerate(days):
      if day.text == today:
        date = day.text
        column = idx
        break
    #print(date, idx)
    #print(table)
    
    for row in table[1:]:
      line = row.find_all("td")
      #jidlo = line[column].text.strip()
      jidlotext = line[column].text.strip()
      jidlo = re.sub(r'^A: [0-9\,]+', '', jidlotext).strip()
      # print (jidlo)
      arr = [ jidlo, '-' ]
      items.append(arr)
    

    return (date, items)

def debug_print(date, menu):
    print(date)
    print(menu)

def result():
    lokalita = "brumlovka"
    try:
        #page = get_file()
        page = get_content()
        date, menu_list = return_menu(page)
        nazev = get_name()
        url = get_url()


        return (nazev, url, date, menu_list, lokalita)
    except:
        #return(get_name() + " - Chyba", "", "Chyba", ["", "", ""])
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [], lokalita)

    os.remove(TMP)

if __name__ == "__main__":
    page = get_content()
    # page = ''
    date, menu_list = return_menu(page)
    debug_print(date, menu_list)
    #print(result())
