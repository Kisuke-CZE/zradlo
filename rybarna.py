#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

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
    a = soup.find("div", { "class": "entry-content" }).find_all("p")
    items = []
    # Protoze polevka je z nejakeho duvodu mimo zbytek menu, projizdim ho zbytecne 2x - ale bylo to nejjednodusi :)
    for item in a:
        #print(item)
        text = item.text
        match = re.match("([\w\d\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ\"\(\)\,\-\{\}]+)[\s]+([0-9\/]+)$", text)
        if match is not None:
            arr = [match.group(1).strip(), match.group(2).strip() + " Kč"]
            items.append(arr)
        else:
            continue
    a = soup.find("div", { "class": "entry-content" }).find("ol").find_all("li")
    for item in a:
        # print(item)
        text = item.text
        match = re.match("([\w\d\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ\"\(\)\,\-\{\}]+)[\s]+([0-9]{2,3})$", text)
        if match is not None:
            arr = [match.group(1).strip(), match.group(2).strip() + " Kč"]
            items.append(arr)
        else:
            continue

    return(items)

def return_date(soup):
    # today = time.strftime("%-d.%-m.%Y")
    # print(today)
    date = "???"
    a = soup.find("div", { "class": "entry-content" }).find_all("p")
    for item in a:
      match = re.match("([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4})", item.text.strip())
      if match:
          date = match.group(1)
          break
    return(date)


def result():
    lokalita = "brumlovka"
    try:
        file = get_file()

        bs = prepare_bs(file)

        nazev = get_name()
        url = get_url()
        date = return_date(bs)

        menu_list = return_menu(bs)

        return (nazev, url, date, menu_list, lokalita)
    except Exception as e:
        print(e)
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [], lokalita)

if __name__ == "__main__":
    file = get_file()

    bs = prepare_bs(file)
    date = return_date(bs)
    menu_list = return_menu(bs)
    print (date, menu_list)
