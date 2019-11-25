#!/usr/bin/env python3
# coding=utf-8
# VRTULE

import requests, os, re, tempfile, time, locale

from bs4 import BeautifulSoup
from subprocess import check_output

locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "http://menu.perfectcanteen.cz/pdf/24/cz/price/a3"

def get_file():
    print("Stahuji menu")
    pdf_stream = requests.get(get_url(), stream=True, timeout=3)
    tmp_fd,tmp_path = tempfile.mkstemp()
    with open(tmp_path, "wb") as f:
      for chunk in pdf_stream.iter_content(chunk_size=1024):
        f.write(chunk)
    os.close(tmp_fd)

    print("menu stazeno, prevadim na text")
    antiword = check_output(["pdftotext", "-layout", tmp_path, "-"]).decode("utf8")
    os.remove(tmp_path)
    print("prevedeno na text")
    return antiword

def get_name():
    return "Perfect Canteen Moneta"

def return_menu(antiword):
    # datum
    today = time.strftime("%A")
    items = []
    published = False
    date = "???"

    for item in antiword.splitlines():
        match = re.match("\s*([A-Za-z0-9ěščřžýáíéůúťňóöďŤĚŠČŘŽŇÝÁÍÉÚŮÓÖĎ \t,\-–“\(\)´\/]+)[\s\n]+([0-9]+)\s+Kč?\s*", item)
        # print(item)
        if match and published:
            # print(item)
            nazev = re.sub(r'\s+', ' ',match.group(1).strip())
            if match.group(2):
                cena = match.group(2).strip()
            if nazev and cena:
                items.append([nazev, cena + ' Kč'])
                continue
        match_date = re.match("(" + today + ").*$", item.strip())
        if match_date:
            date = match_date.group(1)
            published = True

        if published and items and not item.strip():
            break

    return (date, items)

def debug_print(date, menu):
    print(date)
    print(menu)

def result():
    lokalita = "brumlovka"
    try:
        page = get_file()
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
    page = get_file()
    date, menu_list = return_menu(page)
    debug_print(date, menu_list)
    #print(result())
