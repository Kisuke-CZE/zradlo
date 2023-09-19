#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
# from datetime import datetime
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "https://www.roastgrill.cz/"

def get_name():
    return "Roast & Grill Filadelfie"

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

    a = soup.find("div", { "class": "welcome" }).find_all("span")
    #print(a)
    date = "???"
    today = time.strftime("%A %-d.%-m.%Y")
    published = False
    #print(today)
    items = []
    for item in a:
        #print(item.text)
        #matchjidlo = re.match("^[0-9]\.[\s ]+([A-Za-z0-9ěščřžýáíéůúťňóöďŤĚŠČŘŽŇÝÁÍÉÚŮÓÖĎ/ ,\-–“\(\)´]+)[\s ]+([0-9]+\s?Kč)", item.text.strip())
        matchjidlo = re.match("^[\s]*([A-Za-z0-9ěščřžýáíéůúťňóöďŤĚŠČŘŽŇÝÁÍÉÚŮÓÖĎ/ ,\-–“\(\)´]+)[\s ]+([0-9]+\s?Kč)", item.text.strip())
        # matchpolevka = re.match("^Polévka dne:[\s ]+([A-Za-z0-9ěščřžýáíéůúťňóöďŤĚŠČŘŽŇÝÁÍÉÚŮÓÖĎ/ ,\-–“\(\)´]+)[\s ]+([0-9]+\s?Kč[\s ]+/[\s ]+k jídlu 30\s?Kč)", item.text.strip())
        matchpolevka = re.match("^Polévka dne:[\s ]+([A-Za-z0-9ěščřžýáíéůúťňóöďŤĚŠČŘŽŇÝÁÍÉÚŮÓÖĎ/ ,\-–“\(\)´]+)[\s ]+([0-9]+\s?Kč[\s ]+/[\s ]+bez jídla [0-9]+\s?Kč)", item.text.strip())
        if item.text.strip() == today:
            date = item.text.strip()
            published = True
            continue
        elif published and matchpolevka:
            arr = [matchpolevka.group(1).strip(), matchpolevka.group(2).strip()]
            items.append(arr)
            continue
        elif published and matchjidlo:
            arr = [matchjidlo.group(1).strip(), matchjidlo.group(2).strip()]
            items.append(arr)
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

    menu_list, date = return_menu(bs)
    print (date, menu_list)
