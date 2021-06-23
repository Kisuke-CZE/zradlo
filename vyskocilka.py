#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
# from datetime import datetime
from bs4 import BeautifulSoup

def get_url():
    return "http://www.vyskocilka-restaurace.cz/denni-menu/"

def get_name():
    return "Vyskočilka"

def get_file():
    kantyna = requests.get(get_url())
    kantyna.encoding = 'WINDOWS-1250'
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    else:
        return "Error"

def return_menu(soup):

    a = soup.find("div", { "class": "text" })
    #print(a)
    date = a.find("h3").find("strong").text.strip()
    # print(date)
    zradla = a.find_all("th") + a.find_all("td")
    #print (zradla)
    items = []
    for item in zradla:
        # print(item)
        if item.text:
            text = item.text
            #print(text)
            arr = []
            match = re.match("([\w\d\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ\"\(\)\,\-]+)[\s]+([0-9]{2,3}[\s]*,-)", text)
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
