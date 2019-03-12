#!/usr/bin/env python3
# coding=utf-8
# VRTULE

import requests, os, re, tempfile

from bs4 import BeautifulSoup
from subprocess import check_output

_,TMP = tempfile.mkstemp()

def get_url():
    return "http://uvrtulejidelna.webnode.cz/sluzby/"

def get_file():
    response = requests.get(get_url())

    if response.status_code != 200:
        raise requests.RequestException("Error: Vrtule response error")
    html = response.text
    bs = BeautifulSoup(html, "html.parser")

    content_div = bs.find_all("div", {"class": "box_content"})[-1]

    for a in content_div.find_all("a", href=True):
        url = a["href"]
        if ".doc" in url:
            doc_url = url

    doc_stream = requests.get(doc_url, stream=True)
    with open(TMP, "wb") as f:
        for chunk in doc_stream.iter_content(chunk_size=1024):
            f.write(chunk)



    antiword = check_output(["antiword", TMP]).decode("utf8")
    return antiword

def get_name():
    return "Vrtule"

def return_menu(antiword):
    # datum
    lines = [l for l in antiword.split("\n") if l]
    #print(lines)
    jidla = []
    date = "???"
    for item in lines:
        # print(item)
        a = re.match("\s*([0-9]+g)\s+(.*?)\s+([0-9]+\s+Kč)", item)
        c = re.match("\s+?\s+(.*?)\s+([0-9]+\s+Kč)", item) # polivky
        b = re.match("\s+?(([A-Za-zěščřžýáíéúůĚŠČŘŽÝÁÍÉÚŮ]+)\s+[0-9]+\.\s?[0-9]+\s?\.\s?[0-9]+)", item)
        if a:
            #print(a.group(1), a.group(2), a.group(3))
            gramaz = a.group(1)
            jidlo = a.group(2)
            cena = a.group(3)
            jidla.append([jidlo, cena, gramaz])
        elif b:
            date = b.group(1)
        elif c:
            gramaz = ""
            jidlo = c.group(1)
            cena = c.group(2)
            jidla.append([jidlo, cena, gramaz])

    return (date, jidla)

def debug_print(date, menu):
    print(date)
    print(menu)

def result():
    try:
        page = get_file()
        date, menu_list = return_menu(page)
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"

        return (nazev, url, date, menu_list, lokalita)
    except:
        #return(get_name() + " - Chyba", "", "Chyba", ["", "", ""])
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"
        return (nazev, url, "Menu nenalezeno", [], lokalita)

    os.remove(TMP)

if __name__ == "__main__":
    page = get_file()
    date, menu_list = return_menu(page)
    os.remove(TMP)
    #debug_print(date, menu_list)
    #print(result())
