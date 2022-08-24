#!/usr/bin/env python3
# coding=utf-8
# VRTULE

import requests, os, re, tempfile, time, locale

from bs4 import BeautifulSoup
import cv2
import pytesseract
from datetime import datetime, timedelta

locale.setlocale(locale.LC_ALL,'')

def get_url():
    return "https://www.sfood.cz/delta"

def get_content():
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

def get_name():
    return "Lunchbox Delta"

def change_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v,value)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def return_menu(menu):


    #print(menu)
    image = menu.find("div", {"class": "image-wrapper" }).find("noscript").find("img")["src"]
    #print(image)

    tmp_fd,tmp_path = tempfile.mkstemp(suffix = '.png')
    doc_stream = requests.get(image, stream=True, timeout=6)
    with open(tmp_path, "wb") as f:
        for chunk in doc_stream.iter_content(chunk_size=1024):
            f.write(chunk)
    os.close(tmp_fd)
    #print(tmp_path)

    img = cv2.imread(tmp_path)

    img_darkened = change_brightness(img, value=-35) #decreases

    #cv2.imshow('Black white image', img_darkened)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    img_gray = cv2.cvtColor(img_darkened, cv2.COLOR_BGR2GRAY)
    #img_denoised = cv2.medianBlur(img_gray,1)
    #img_tresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img_tresh = cv2.threshold(img_gray, 120, 255, cv2.THRESH_BINARY)[1]
    img_inverted=cv2.bitwise_not(img_tresh)

    #cv2.imshow('Black white image', img_inverted)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    tesseract_config = r'--oem 3 --psm 3'
    menutext = pytesseract.image_to_string(img_inverted, lang="ces", config=tesseract_config)
    #print(menutext)
    os.remove(tmp_path)

    # datum
    today = time.strftime("%A")
    #today = "Čtvrtek"
    tomorrow = (datetime.now() + timedelta(1)).strftime("%A")
    #print(today)
    #print(tomorrow)
    items = []
    published = False
    previous = ""
    date = "???"
    for item in menutext.splitlines():
        #print(item)
        match = re.match("([\w\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ,\-\/]+).*\s+([0-9]{2,3}\s+Kč)", item)
        if match and published:
            #print("Match")
            if previous:
                arr = [previous + " " + match.group(1).strip(), match.group(2).strip()]
                previous = ""
            else:
                arr = [match.group(1).strip(), match.group(2).strip()]
            items.append(arr)
        elif not published and item.strip() == today:
            #print(item)
            date = item.strip()
            published = True
        elif published and item.strip() == tomorrow:
            #print(item)
            break
        elif not match and published:
            again = re.match("([\w\sěščřžýáíéúůóÓĚŠČŘŽÝÁÍÉÚŮöäëÄÖËťŤ,\-\/]+)", item)
            if again:
                previous = again.group(1).strip()
                #print(item)
                #print("Match")
            else:
                previous = ""
                #print("Blank")

        #elif published:
        #    published = False
        #    break

    return (date, items)

def debug_print(date, menu):
    print(date)
    print(menu)

def result():
    lokalita = "brumlovka"
    try:
        #page = get_file()
        page = get_content()
        bs = prepare_bs(page)
        date, menu_list = return_menu(bs)
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
    page = get_content()
    bs = prepare_bs(page)
    date, menu_list = return_menu(bs)
    debug_print(date, menu_list)
    #print(result())
