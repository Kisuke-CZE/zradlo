#!/usr/bin/env python3
# coding=utf-8
import requests, sys, re
from datetime import datetime
from bs4 import BeautifulSoup

def get_file():
	kantyna = requests.get("http://www.kolkovna.cz/cs/kolkovna-argentinska-23/denni-menu")
	return kantyna

def prepare_bs(kantyna):
	if kantyna is not None and kantyna.status_code == 200:
		html = kantyna.text
		soup = BeautifulSoup(html, 'html.parser')
		return soup

	else:
		return "Error"

def return_menu(soup):
	
	#b = a.findNext("dm-day").text
	#c = b.findNext("p").text
	#d = re.split(" Kč", c)
	
	meme = soup.find("div", { "class": "dailyMenuWeek" })
	test = meme.find_all("section")
	denvtydnu = datetime.today().weekday()
	dnesni = test[denvtydnu%5].find_all("tr") # o vikendu nezerem
	date = test[denvtydnu%5].find_all("h2")[0].text
	arr = []
	for i in dnesni:
		arr.append(["{0} - {1}".format(i.findNext("td", { "class": "title"} ).text, i.findNext("td", { "class": "name"} ).text), i.findNext("td", { "class": "price"} ).text])
	print(arr)

#	jidlo_obsah = soup.find_all("span", { "class": "td-jidlo-obsah"} )
#	jidlo_cena =  soup.find_all("td", { "class": "td-cena"} )
#	arr = []
#	for i in range(0, len(jidlo_obsah)):
#		arr.append([jidlo_obsah[i].text, jidlo_cena[i].text])

	items = arr	
	

	print("ITEMS {0}".format(items))
	print("DATE", date)
	return(items, date)


#def return_date(soup):
#	return("")

def result():
	try:
		file = get_file()

		bs = prepare_bs(file)

		#date = return_date(bs)
		menu_list, date = return_menu(bs)

		return(date, menu_list)
	except Exception as e:
		print(e)
		return(str(e), [])

if __name__ == "__main__":
	file = get_file()

	bs = prepare_bs(file)

	#date = return_date(bs)
	menu_list = return_menu(bs)

	#debug_print(date, menu_list)
