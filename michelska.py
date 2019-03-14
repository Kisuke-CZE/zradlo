#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "http://www.michelska.cz/dnes.htm"

def get_name():
    return "Michelská"

def get_file():
    kantyna = requests.get(get_url())
    kantyna.encoding = 'Windows-1250'
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    else:
        return "Error"

def return_menu(soup):
    date = soup.find_all("p", {"class": "MsoNormal"})[1].text.strip().strip('Nabídka na')
    a = soup.find("table").find_all("tr")
    items = []
    for item in a:
        # print(item)
        grid = item.find_all("td")
        jidlo = grid[1].text.strip()
        # print(grid[2].text)
        predcena = re.match("([0-9]{2,3}[\s]*,-).*", grid[2].text.strip())
        if predcena:
            cena = predcena.group(1).strip()
            if jidlo and cena:
                arr = [jidlo, cena]
                items.append(arr)
            else:
                continue
        else:
            continue
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

    # menu_list, date = return_menu(bs)
    # print (date, menu_list)
