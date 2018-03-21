#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, time, locale
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "http://extolinn.cz/main/daily_menu"

def get_name():
    return "Extol Inn"

def get_file():
    user_agent = {
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Language': 'cs,sk;q=0.8,en-US;q=0.5,en;q=0.3',
                  'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0',
                  }
    session = requests.Session()
    r = session.get("http://extolinn.cz/main/set_lang/czech", headers = user_agent)
    #print(r.cookies)
    kantyna = session.get(get_url(), headers = user_agent)
    return kantyna

def prepare_bs(kantyna):
    if kantyna is not None and kantyna.status_code == 200:
        html = kantyna.content
        soup = BeautifulSoup(html.decode('utf-8', 'ignore'), 'html.parser')
        return soup

    else:
        return None

def return_menu(soup):
    a = soup.find_all("div", { "class": "container" })[1].find_all("div" )


    #print (jidlo_obsah)

    jidlo_cena = []
    items = []
    today = time.strftime("%A - %d.%m.%Y")
    published = False
    # print(today)
    date = "???"
    for i in a:
      if published:
          jidlo_obsah = i.find_all("tr")
          for line in jidlo_obsah:
            zradlo = line.find_all("td")
            # print (zradlo)
            nazev = zradlo[2].text
            cena = zradlo[3].text
            # print(cena)
            # print(nazev)
            arr = [nazev, cena]
            items.append(arr)
          break

      if i.text.strip() == today:
          published = True
          date = today

    return(items, date)

def result():
    try:
        file = get_file()

        bs = prepare_bs(file)

        #date = return_date(bs)
        nazev = get_name()
        url = get_url()

        menu_list, date = return_menu(bs)

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
    # menu_list, date = return_menu(bs)
    # print(date, menu_list)
