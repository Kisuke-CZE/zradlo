#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from bs4 import BeautifulSoup

# locale.setlocale(locale.LC_ALL,'cs_CZ.UTF-8')
locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "http://www.silencio.cafe/kde-nas-najdete/"
    #return "http://restauracehamburg.cz/homepage/poledni-menicka"

def get_name():
    return "Silencio Café"

def get_file():
    kantyna = requests.get("http://www.silencio.cafe/denni-nabidka/")
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.content
        soup = BeautifulSoup(html.decode('utf-8', 'ignore'), 'html.parser')
        return soup

    else:
        return None

def return_menu(soup):
    today = time.strftime("%A")
    #print(today)
    items = []
    published = False
    date = "???"
    date = today+" "+soup.find("div", { "class": "et_pb_text et_pb_module et_pb_bg_layout_dark et_pb_text_align_center et_pb_text_0" }).p.text.strip()
    days = soup.find_all("div", { "class": "et_pb_toggle" })
    #print(days)
    for day in days:
        dow = day.h5.text
        if dow == today:
            jidla = day.find_all("strong")
            for jidlo in jidla:
                items.append([jidlo.text, ""])
    #print(soup)
    #print(date)


    return(date, items)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)

        #date = return_date(bs)
        nazev = get_name()
        url = get_url()

        date, menu_list = return_menu(bs)

        return(nazev, url, date, menu_list)
    except Exception as e:
        print(e)
        #return (get_name() + "- Chyba", "", str(e), [])
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [])

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    # date, menu_list = return_menu(bs)
    # print(date, menu_list)

    #debug_print(date, menu_list)
