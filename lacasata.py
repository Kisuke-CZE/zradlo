#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from bs4 import BeautifulSoup

# locale.setlocale(locale.LC_ALL,'cs_CZ.UTF-8')
locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "http://www.lacasata.cz/"

def get_name():
    return "La Casata"

def get_file():
    user_agent = {'User-agent': 'Mozilla/5.0'}
    kantyna = requests.get(get_url(), headers = user_agent)
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.content
        soup = BeautifulSoup(html.decode('utf-8', 'ignore'), 'html.parser')
        return soup

    else:
        return None

def return_menu(soup):
    #today = time.strftime("%A %-d.%-m.%Y").upper()
    today = time.strftime("%A %-d.%-m.").upper()

    print(today)
    items = []
    published = False
    date = "???"
    a = soup.find("div", {"class": "element_content_box_4"}).find("div", {"class": "content"}).text
    #print(a)
    for item in a.splitlines():
        #print(item)
        match = re.match("([\w\d\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ–\"\(\)\,\-]+)[\s]+([0-9]{2,3},-)", item)
        if match and published:
            arr = [match.group(1).strip(), match.group(2).strip()]
            items.append(arr)
        elif not published and item.strip().upper() == today:
            date = item.strip()
            published = True
        elif published:
            published = False
            break

    return(date, items)

def result():
    lokalita = "brumlovka"
    try:
        file = get_file()

        bs = prepare_bs(file)

        #date = return_date(bs)
        nazev = get_name()
        url = get_url()

        date, menu_list = return_menu(bs)

        return(nazev, url, date, menu_list, lokalita)
    except Exception as e:
        print(e)
        #return (get_name() + "- Chyba", "", str(e), [])
        nazev = get_name()
        url = get_url()

        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)

    #date = return_date(bs)
    date, menu_list = return_menu(bs)
    print(date, menu_list)

    #debug_print(date, menu_list)
