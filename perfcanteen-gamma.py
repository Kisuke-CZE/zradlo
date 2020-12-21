#!/usr/bin/env python3
# coding=utf-8
# VRTULE

import requests, os, re, tempfile, time, locale

from bs4 import BeautifulSoup
from subprocess import check_output

locale.setlocale(locale.LC_ALL,'')



def get_url():
    return "http://menu.perfectcanteen.cz/menu/getmenu/8/cz/pdf/price"

def get_file():
    print("Stahuji menu")
    pdf_stream = requests.get(get_url(), stream=True, timeout=6)
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
    return "Perfect Canteen Gamma"

def return_menu(antiword):
    # datum
    today = time.strftime("%A")
    # today = "Pátek"
    items = []
    published = False
    prev_match = False
    date = "???"

    for item in antiword.splitlines():
        match = re.match("\s*([A-Za-z0-9ěščřžýáíéůúťňóöďŤĚŠČŘŽŇÝÁÍÉÚŮÓÖĎ \t,\-–“\(\)´\/]+)[\s\n]+([0-9]+)\s+Kč?\s*", item)
        # print(item)
        match_date = re.match("(" + today + ").*$", item.strip())
        if match and published:
            # print(item)
            nazev = re.sub(r'\s+', ' ',match.group(1).strip())
            if match.group(2):
                cena = match.group(2).strip()
            if nazev and cena:
                items.append([nazev, cena + ' Kč'])
                # prev_match = True
                continue
        elif match_date:
            date = match_date.group(1)
            published = True
            # prev_match = True
        elif published and not item.strip() and prev_match:
            prev_match = False
            continue
        elif published and not item.strip() and not prev_match:
            break
        elif not match:
            prev_match = False
            continue

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
    # print(result())
