#!/usr/bin/env python3
# coding=utf-8
# VRTULE

import requests, os, re, tempfile, time, locale, pdfplumber

from bs4 import BeautifulSoup
from subprocess import check_output

locale.setlocale(locale.LC_ALL,'')

def get_url():
    # return "http://officefood.cz/wp-content/uploads/filadelfie.pdf"
    url = "https://www.cantina-lafresca.cz/menu/brumlovka"
    print("Zjistuji URL menu")
    response = requests.get(url, timeout=6)
    if response.status_code != 200:
        raise requests.RequestException("Error: Lafresca response error")
    html = response.text
    bs = BeautifulSoup(html, "html.parser")
    button_url = bs.find("a", {"title": "Zobrazit menu"})
    if button_url:
      doc_url = "https://www.cantina-lafresca.cz" + button_url['href']
      return doc_url
    else:
      return None

def get_content():


    print("Stahuji menu")
    url=get_url()
    if not url:
        print("Nelze ziskat URL menu")
        return None
    pdf_stream = requests.get(get_url(), stream=True, timeout=6)
    #tmp_fd,tmp_path = tempfile.mkstemp()
    tmp_fd,tmp_path = tempfile.mkstemp(suffix = '.pdf')
    with open(tmp_path, "wb") as f:
      for chunk in pdf_stream.iter_content(chunk_size=1024):
        f.write(chunk)
    os.close(tmp_fd)

    with pdfplumber.open(tmp_path) as pdf_menu:
      #table = pdf_menu.pages[0].extract_table(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines", "join_tolerance": 30})
      table = pdf_menu.pages[0].extract_table(table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines", "join_y_tolerance": 30, "join_x_tolerance": 30, "snap_tolerance": 10})

    os.remove(tmp_path)
    print("prevedeno na tabulky")

    # SOME DEBUGGING
    #print(table)
    #import pandas as pd
    #pd.set_option('display.max_columns', None)
    #print(pd.DataFrame(table))

    return table

def get_name():
    return "La Fresca Filadelfie"

def return_menu(menu):
    # datum
    today = time.strftime("%A %d.%m.%Y")
    #print(today)
    items = []
    #items.append(['Menu se nedari rozparsovat - zatim jen odkaz', '∞ Kč'])

    cellnum=0
    for menuday in menu[0]:
      if menuday.replace('\n', ' ') == today:
        # print(today)
        date = today
        break
      cellnum+=1

    menulength=(len(menu))
    for row in range(1, menulength):
      #print(menu[row][cellnum])
      #print(menu[row][0])
      jidlo = menu[row][cellnum].split('A:')[0]
      #cena = menu[row][0].split('\n')[1]
      cena = menu[row][0].split('\n')[-1]
      # print(cena)
      items.append([jidlo, cena])


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
