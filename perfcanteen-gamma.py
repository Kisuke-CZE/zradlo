#!/usr/bin/env python3
# coding=utf-8
# VRTULE

import requests, os, re, tempfile, time, locale

from bs4 import BeautifulSoup
from subprocess import check_output

locale.setlocale(locale.LC_ALL,'')

_,TMP = tempfile.mkstemp()

def get_url():
    return "http://menu.perfectcanteen.cz/menu/getmenu/8/cz/pdf/price"

def get_file():
    pdf_stream = requests.get(get_url(), stream=True)
    with open(TMP, "wb") as f:
        for chunk in pdf_stream.iter_content(chunk_size=1024):
            f.write(chunk)



    antiword = check_output(["pdftotext", "-layout", TMP, "-"]).decode("utf8")
    return antiword

def get_name():
    return "Perfect Canteen Gamma"

def return_menu(antiword):
    # datum
    today = time.strftime("%A")
    items = []
    published = False
    date = "???"

    for item in antiword.splitlines():
        match = re.match("\s*([A-ZĚŠČŘŽÝÁÍÉÚŮŤŇÓÖ][A-Za-z0-9ěščřžýáíéůúťňóöŤĚŠČŘŽŇÝÁÍÉÚŮÓÖ \t,\-–“\(\)´\/]+)[\s\n]+([0-9]+)\s+Kč?\s*", item)
        if match and published:
            nazev = re.sub(r'\s+', ' ',match.group(1).strip())
            if match.group(2):
                cena = match.group(2).strip()
            if nazev and cena:
                items.append([nazev, cena + ' Kč'])

        if item.strip() == today:
            date = item.strip()
            published = True

        if published and not item.strip():
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
    os.remove(TMP)
    debug_print(date, menu_list)
    #print(result())
