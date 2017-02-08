#!/usr/bin/env python3
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from datetime import datetime

import locale
locale.setlocale(locale.LC_TIME, "cs_CZ.UTF-8")

from kantyna import result as kantyna # KANTYNA
from kozlovna import result as kozlovna # KOZLOVNA
from vrtule import result as vrtule # VRTULE
from kolkovna import result as kolkovna # KOLKOVNA

app = Flask(__name__)
app.config["STATIC_FOLDER"] = "static"

@app.route("/", methods=["GET"])
def home():
    try:
        a = kantyna() or ["", ""]
    except:
        a = ["", ""]

    try:
        b = kozlovna() or ["", ""]
    except:
        b = ["", ""]

    try:
        c = vrtule() or ["", ""]
    except:
        c = ["", ""]

    try:
        d = kolkovna() or ["", ""]
    except:
        d = ["", ""]

    return render_template("home.html", dnesni_datum=datetime.today().strftime("%A %d. %m. %Y"), 
    	date=a[0],
    	menu=a[1],
    	date2=b[0],
    	menu2=b[1],
    	date3=c[0],
    	menu3=c[1],
        date4=d[0],
        menu4=d[1],
        )

if __name__ == "__main__":
    app.run(debug=True)

