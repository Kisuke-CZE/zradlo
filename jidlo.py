#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from datetime import datetime
import importlib
from flask.ext.cache import Cache

import locale
locale.setlocale(locale.LC_TIME, "cs_CZ.UTF-8")

#from kantyna import result as kantyna # KANTYNA
#from kozlovna import result as kozlovna # KOZLOVNA
#from vrtule import result as vrtule # VRTULE
#from kolkovna import result as kolkovna # KOLKOVNA

cache = Cache(config={'CACHE_TYPE': 'simple'})

modules = ["kantyna", "kozlovna", "vrtule", "avion58", "kolkovna", "pinta", "uholise", "motoburger", "hamburg", "baterka", "port_stanley", "petpenez", "jatka78", "port58"]
imported = []
for i in modules:
    imported.append(importlib.import_module(i, __name__))
app = Flask(__name__)
app.config["STATIC_FOLDER"] = "static"
cache.init_app(app)

@app.route("/", methods=["GET"])
@cache.cached(timeout=720)
def home():
    nazvy = []
    urlka = []
    jidla = []
    datumy = []

    for y in imported:
        nazev, url, datum, jidlo = y.result()
        nazvy.append(nazev)
        urlka.append(url)
        jidla.append(jidlo)
        datumy.append(datum)
    print("Importing:", nazvy, urlka, jidla, datumy)

    return render_template("home.html", dnesni_datum=datetime.today().strftime("%A %d. %m. %Y"), nazvy=nazvy, urlka=urlka, jidla=jidla, datumy=datumy)


if __name__ == "__main__":
    app.run(debug=True)
