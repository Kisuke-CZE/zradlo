#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from datetime import datetime
from bs4 import BeautifulSoup
locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "http://rybarna.net/denni-menu/"

def get_name():
    return "Rybárna"

def get_file():
    kantyna = requests.get(get_url())
    kantyna.encoding = 'UTF-8'
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.text
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    else:
        return "Error"

def return_menu(soup):

    a = soup.find("div", { "class": "entry-content" }).find("ol").find_all("li")
    items = []
    for item in a:
        # print(item)
        text = item.text
        match = re.match("([\w\d\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ\"\(\)\,\-\{\}]+)[\s]+([0-9]{2,3})$", text)
        if match is not None:
            arr = [re.sub('[{}]', '',match.group(1).strip()), match.group(2).strip() + " Kč"]
        else:
            continue
        items.append(arr)

    return(items)

def return_date(soup):
    today = time.strftime("%-d.%-m.%Y")
    # print(today)
    date = "???"
    a = soup.find("div", { "class": "entry-content" }).find_all("p")
    for item in a:
      if item.text == today:
          date = item.text
    return(date)


def result():
    lokalita = "brumlovka"
    try:
        file = get_file()

        bs = prepare_bs(file)

        nazev = get_name()
        url = get_url()

        menu_list, date = return_menu(bs)

        return (nazev, url, date, menu_list, lokalita)
    except Exception as e:
        print(e)
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)
    #date = return_date(bs)
    #menu_list = return_menu(bs)
    #print (date, menu_list)
