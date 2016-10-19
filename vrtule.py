#!/usr/bin/env python3
# coding=utf-8
# VRTULE

import requests, sys, re, codecs

# TODO: POLIVKY+posledni radky, co nemaj \t
# TODO: POLIVKY+posledni radky, co nemaj \t
# TODO: POLIVKY+posledni radky, co nemaj \t
# TODO: POLIVKY+posledni radky, co nemaj \t
# TODO: POLIVKY+posledni radky, co nemaj \t

def return_menu():
	fs = codecs.open("vrtule.txt", "r", "utf-8")
	vrt = fs.read()
	fs.close()
	jidla = []
	date = "???"

	for item in vrt.split("\n"):
		#([0-9]+g)\s+(.*?)\s+([0-9]+\s+Kč)
		a = re.match("\s+?([0-9]+g)\s+(.*?)\s+([0-9]+\s+Kč)", item)
		b = re.match("\s+?((Pondělí|Úterý|Středa|Čtvrtek|Pátek)\s+[0-9]+\.\s+[0-9]+\.\s+[0-9]+)", item)
		if a is not None:
			print(a.group(1), a.group(2), a.group(3))
			gramaz = a.group(1)
			jidlo = a.group(2)
			cena = a.group(3)
			jidla.append([jidlo, cena, gramaz])
			#jidla.append(["{0}{1}".format(a.group(1), a.group(2))], a.group(3))
		elif b is not None:
			date = b.group(1)
		else:
			pass

	return (date, jidla)

def debug_print(date, menu):
	print(date, menu)

def result():
	try:
		date, menu_list = return_menu()

		debug_print(date, menu_list)
		return(date, menu_list)
	except:
		return("Chyba", ["", "", ""])

if __name__ == "__main__":
	date = return_date()
	menu_list = return_menu()
	print(menu_list)

