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
    fulldate = time.strftime("%-d. %-m. %Y")
    # print(dow + " " + fulldate)
    #dow = "PONDĚLÍ"
    #fulldate = "21. 11. 2022"
    tablenum=1
    
    #a = soup.find("div", { "class": "daily-menu" }).div.find_next_sibling("div").div.div
    a = soup.find("div", { "class": "daily-menu" }).div.div.div
    #print(a)

    dates = a.find_all("h4", { "class": "weekday", "data-lang": "cz"})
    lasttab = 1
    for index,item in enumerate(dates):
        datematch = re.match(dow + "\\s+" + fulldate, item.text.strip(), re.IGNORECASE)
        lasttab = index
        # print(item.text.strip())
        if datematch:
            tablenum = index

    date = dates[tablenum].text.strip()
    tables = a.find_all("table", recursive=False)
    # lasttab = 4 * tablenum
    # lasttab = 5 * tablenum
    items = []
    # matchzradlo = "([\\w\\d\\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ„“\"\\(\\)\\,\\-\\+]+)[\\s]+([0-9]{2,3}[\\s]*(Kč|,-))"
    zradla = tables[tablenum].find_all("tr", recursive=False)
    for item in zradla:
      #if item.text:
      #  text = item.text
      #  arr = []
      #  match = re.match(matchzradlo, text)
      #  if match is not None:
      #    arr = [match.group(1).strip(), match.group(2).strip()]
      #  else:
      #    continue
      if item.td.span is None:
        continue
      nazev = item.td.find("span", { "data-lang": "cz" }).text.strip()
      cena = item.find_all("td")[1].text.strip()
      arr = [nazev, cena]
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
