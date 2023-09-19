#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from datetime import datetime
import importlib
# from flask.ext.cache import Cache
from flask_caching import Cache

import locale
locale.setlocale(locale.LC_TIME, "cs_CZ.UTF-8")

cache = Cache(config={'CACHE_TYPE': 'simple'})

modules = [ "kozlovna",
            "kolkovna-artgen",
            "avion58",
            "vrtule",
            "petpenez",
            "hamburg",
            "baterka",
            "jatka78",
            "kantyna",
            "lunchbox-gamma",
            "perfcanteen-moneta",
            "turnovska-brumlovka",
            "lunchbox-delta",
            "lunchbox-alpha",
            "filadelfie",
            "roastgrill",
            "cervena-cibule",
            "ukubika",
            "pragos",
            "michelska",
            "nesmysl",
            "kolkovna-budej",
            "nakopecku",
            "melina",
            "antal",
            "rybarna"
             ]
imported = []
for i in modules:
    imported.append(importlib.import_module(i, __name__))
app = Flask(__name__)
app.config["STATIC_FOLDER"] = "static"
cache.init_app(app)

@app.route("/", methods=["GET"])
@cache.cached(timeout=1800)
def home():
    nazvy = []
    urlka = []
    jidla = []
    datumy = []
    lokality = []
    moduly = []

    for y in imported:
        print(y.__name__)
        nazev, url, datum, jidlo, lokalita = y.result()
        nazvy.append(nazev)
        urlka.append(url)
        jidla.append(jidlo)
        datumy.append(datum)
        lokality.append(lokalita)
        moduly.append(y.__name__)
    print("Importing:", nazvy, urlka, jidla, datumy, lokality, moduly)

    return render_template("home.html", dnesni_datum=datetime.today().strftime("%A %d. %m. %Y"), nazvy=nazvy, urlka=urlka, jidla=jidla, datumy=datumy, lokality=lokality, moduly=moduly)


if __name__ == "__main__":
    app.run(debug=True)
