#!/usr/bin/env python3
# coding=utf-8
# VRTULE

import requests, os, re, tempfile, time, locale

from bs4 import BeautifulSoup
from subprocess import check_output

locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "http://officefood.cz/wp-content/uploads/filadelfie.pdf"

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
    #print(antiword)
    os.remove(tmp_path)
    print("prevedeno na text")
    return antiword

def get_name():
    return "Office Food Filadelfie"

def return_menu(antiword):
    # datum
    today = time.strftime("%A").upper()
    print(today)
    # today = "Pátek"
    items = []
    published = False
    date = "???"
    # print(antiword.splitlines())

    for item in antiword.splitlines():
        match = re.match("^([0-9,]+[gl])?[ ]{2,999}(Polévka A|Polévka B|Česká kuchyně|Standard|Veggie / Sladké|Vital Office|Minutka / Grill|Premium|Pizza / Gyros|Denní salát)[ ]{2,999}([A-Za-z0-9ěščřžýáíéůúťňóöďŤĚŠČŘŽŇÝÁÍÉÚŮÓÖĎ/ ,\-–“\(\)´]+)[ ]{2,999}([0-9]{2,4})Kč$", item)
        #print(item)
        match_date = re.match("(" + today + ").*$", item.strip())
        #someday = re.match("^(?!POLÉVKA)[A-ZŤĚŠČŘŽŇÝÁÍÉÚŮÓÖ]+$", item.strip())
        someday = re.match("(PONDĚLÍ|ÚTERÝ|STŘEDA|ČTVRTEK|PÁTEK|SOBOTA|NEDĚLĚ)$", item.strip())
        if match and published:
            #print(match.group(2))
            #print(item)
            # nazev = re.sub(r'\s+', ' ',match.group(2).strip())
            nazev = match.group(3).strip()
            if match.group(2) == "Pizza / Gyros":
                nazev = nazev + " (" + match.group(2) + ")"
            # print(nazev + ": " + match.group(4))
            if match.group(4):
                cena = match.group(4).strip()
                #print(cena + ": " + match.group(3))
                #print(cena + ": " + match.group(2))
                # nazev = match.group(3).strip()
            if nazev and cena:
                items.append([nazev, cena + ' Kč'])
                prev_match = True
                continue
        elif match_date:
            date = match_date.group(1)
            published = True
        elif published and someday:
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
