#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from bs4 import BeautifulSoup

def get_url():
    #return "http://www.manihi.cz/zavodni-stravovani-kantyna/kantyna-rosmarin-business-center/denni-menu"
    return "http://www.manihi.cz/menu"

def get_name():
    return "Kantýna"

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
    a = soup.find("div", { "class": "content ez cf" }).find_all("div", { "class": "c-c cf" })
    datum = a[1].text.strip().strip('Denní nabídka ')
    #print (datum)
    zradla = a[3].find_all("p")

    items = []
    for item in zradla:
        #print(item)
        if item.text:
            text = item.text
            #print(text)
            arr = []
            match = re.match("([\w\d\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ\"\(\)\,\-]+)[\s]+([0-9]{2,3}[\s]*Kč)", text)
            if match is not None:
                arr = [match.group(1).replace('\xa0', '').strip(), match.group(2).replace('\xa0', '').strip()]
            else:
                continue
            items.append(arr)
    return datum, items


def debug_print(date, menu):
    print(date)
    print(menu)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"
        date = return_date(bs)
        menu_list = return_menu(bs)

        #print(date, menu_list)
        return(nazev, url, date, menu_list, lokalita)
    except Exception as exp:
        print(exp)
        # return(get_name() + "- Chyba", "", "", [str(exp)])
        nazev = get_name()
        url = get_url()
        lokalita = "holesovice"
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)
    date, menu_list = return_menu(bs)
    debug_print(date, menu_list)
