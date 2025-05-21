#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re, tempfile, os
from datetime import datetime
from subprocess import check_output
from bs4 import BeautifulSoup

def get_url():
    return "http://www.michelska.cz/denni-menu"

def get_name():
    return "Michelská"

def get_file():
    print("Stahuji menu")
    user_agent = {'User-agent': 'Mozilla/5.0'}
    menupage = requests.get(get_url(), headers = user_agent)
    antiword = None
    if menupage is not None and menupage.status_code == 200:
      htmlcode = BeautifulSoup(menupage.text, 'html.parser')
      gdrive_link = htmlcode.find("div", {"class": "pdf-iframe-container"} ).find("iframe")['src']
      gdrive_id = re.match(".*file\\/d\\/(.*)\\/preview", gdrive_link)[1]
      gdrive_down = "https://drive.usercontent.google.com/download?id=" + gdrive_id + "&export=download&authuser=0"
      pdf_stream = requests.get(gdrive_down, stream=True, timeout=6)
      # print(gdrive_down)
      tmp_fd,tmp_path = tempfile.mkstemp()
      with open(tmp_path, "wb") as f:
        for chunk in pdf_stream.iter_content(chunk_size=1024):
          f.write(chunk)
      os.close(tmp_fd)
      
      print("menu stazeno, prevadim na text")
      antiword = check_output(["pdftotext", "-layout", tmp_path, "-"]).decode("utf8")
      os.remove(tmp_path)
      print("prevedeno na text")
    return antiword
    
def debug_print(date, menu):
    print(date)
    print(menu)

def return_menu(antiword):
    #print(antiword)
    items = []
    prev_match = False
    date = "???"
    
    for item in antiword.splitlines():
        match = re.match('\\s*([0-9]+[a-z]+)?([A-Za-z0-9ěščřžýáíéůúťňóöďŤĚŠČŘŽŇÝÁÍÉÚŮÓÖĎ \t,\\-–“„\\(\\)´\\/]+)[\\s\n]+([0-9]+)\\s?,-\\s*', item)
        match_date = re.match('Nabídka na (.*)', item.strip())
        if match:
            nazev = match.group(2).strip()
            cena = match.group(3).strip()
            if nazev and cena:
                items.append([nazev, cena + ' Kč'])
                continue
        elif match_date:
            date = match_date.group(1)
    return(date, items)


def result():
    lokalita = "brumlovka"
    try:
        page = get_file()
        date, menu_list = return_menu(page)
        nazev = get_name()
        url = get_url()


        return (nazev, url, date, menu_list, lokalita)
    except:
        #return(get_name() + " - Chyba", "", "Chyba", ["", "", ""])
        nazev = get_name()
        url = get_url()
        return (nazev, url, "Menu nenalezeno", [], lokalita)

    os.remove(TMP)

if __name__ == "__main__":
    page = get_file()
    date, menu_list = return_menu(page)
    debug_print(date, menu_list)
