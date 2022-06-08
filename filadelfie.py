#!/usr/bin/env python3
# coding=utf-8
# VRTULE

import requests, os, re, tempfile, time, locale

from bs4 import BeautifulSoup
from subprocess import check_output

locale.setlocale(locale.LC_ALL,'')

def get_url():
    # return "http://officefood.cz/wp-content/uploads/filadelfie.pdf"
    return "https://www.cantina-lafresca.cz/menu/brumlovka"
    print("Zjistuji URL menu")
    response = requests.get(get_url(), timeout=6)
    if response.status_code != 200:
        raise requests.RequestException("Error: Lafresca response error")
    html = response.text
    bs = BeautifulSoup(html, "html.parser")
    doc_url = "https://www.cantina-lafresca.cz" + bs.find("a", {"title": "Zobrazit menu"})['href']
    print(doc_url)
    return doc_url

def get_file():


    print("Stahuji menu")
    pdf_stream = requests.get(get_url, stream=True, timeout=6)
    tmp_fd,tmp_path = tempfile.mkstemp()
    with open(tmp_path, "wb") as f:
      for chunk in pdf_stream.iter_content(chunk_size=1024):
        f.write(chunk)
    os.close(tmp_fd)

    #print("menu stazeno, prevadim na text")
    #antiword = check_output(["pdftotext", "-layout", tmp_path, "-"]).decode("utf8")
    #antiword = check_output(["pdftotext", "-table", tmp_path, "-"]).decode("utf8")
    print(antiword)
    os.remove(tmp_path)
    print("prevedeno na text")
    return antiword

def get_name():
    return "La Fresca Filadelfie"

def return_menu(antiword):
    # datum
    today = time.strftime("%A").upper()
    items = []
    # date = "???"
    date = today
    items.append(['Menu se nedari rozparsovat - zatim jen odkaz', '∞ Kč'])
    # print(antiword.splitlines())

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
    # page = get_file()
    page = ''
    date, menu_list = return_menu(page)
    debug_print(date, menu_list)
    #print(result())
