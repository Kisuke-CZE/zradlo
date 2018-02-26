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
    a = soup.find_all("div", { "class": "text-content" })[2]
    #print(a)
    while a.p.find("p"):
      a = a.p
    b = a.find_all("p")
    #b = a.find_all("strong")
    items = []
    for item in b:
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
    return items


def return_date(soup):
    b = soup.find_all("div", { "class": "text-content" })
    #print(b)
    b = b[1].find_all('h3')[0].text
    #b = b[0].h3.string
    b = b.replace("Denní nabídka ", "")
    return(b)

def debug_print(date, menu):
    print(date)
    print(menu)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)
        nazev = get_name()
        url = get_url()
        date = return_date(bs)
        menu_list = return_menu(bs)

        #print(date, menu_list)
        return(nazev, url, date, menu_list)
    except Exception as exp:
        print(exp)
        # return(get_name() + "- Chyba", "", "", [str(exp)])
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [])

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    date = return_date(bs)
    menu_list = return_menu(bs)
    # lol()

    #debug_print(date, menu_list)
