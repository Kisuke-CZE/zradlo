#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
# from datetime import datetime
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "https://turnovskapivnice.cz/nase-podniky/brumlovka"

def get_name():
    return "Turnovská pivnice Brumlovka"

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

    #dow = time.strftime("%A").upper()
    #dow = time.strftime("%A").lower()
    dow = time.strftime("%A")
    fulldate = time.strftime("%-d. %-m. %Y").upper()
    #print(dow + " " + fulldate)
    #dow = "PONDĚLÍ"
    #fulldate = "21. 11. 2022"
    tablenum=1

    a = soup.find("div", { "class": "daily-menu" }).div.find_next_sibling("div").div.div
    #print(a)

    dates = a.find_all("h4")
    for index,item in enumerate(dates):
        datematch = re.match(dow + "\s+" + fulldate, item.text, re.IGNORECASE)
        if datematch:
            #print(item.text)
            tablenum = index

    date = dates[tablenum].text
    tables = a.find_all("table", recursive=False)
    #lasttab = 4 * tablenum
    lasttab = 5 * tablenum
    items = []
    matchzradlo = "([\w\d\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ„“\"\(\)\,\-\+]+)[\s]+([0-9]{2,3}[\s]*(Kč|,-))"
    for table in range(lasttab-4, lasttab):
        zradla = tables[table].tbody.find_all("tr", recursive=False)
        for item in zradla:
            #print(item)
            subtables = item.find_all("table")
            if subtables:
                for subtable in subtables:
                    subzradla = subtable.find_all("tr")
                    for subitem in subzradla:
                        subtext = subitem.text
                        arr = []
                        submatch = re.match(matchzradlo, subtext)
                        if submatch is not None:
                            arr = [submatch.group(1).strip(), submatch.group(2).strip()]
                            items.append(arr)
                        else:
                            continue

            elif item.text:
                text = item.text
                arr = []
                match = re.match(matchzradlo, text)
                if match is not None:
                    arr = [match.group(1).strip(), match.group(2).strip()]
                else:
                    continue
                items.append(arr)

    return(items, date)


def result():
    try:
        file = get_file()

        bs = prepare_bs(file)

        nazev = get_name()
        url = get_url()
        lokalita = "brumlovka"

        menu_list, date = return_menu(bs)

        return (nazev, url, date, menu_list, lokalita)
    except Exception as e:
        print(e)
        nazev = get_name()
        url = get_url()
        lokalita = "brumlovka"
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    menu_list, date = return_menu(bs)
    print (date, menu_list)
