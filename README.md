# Zradlo
### Stránka pro agregaci jídelníčku poblíž ulic Argentinská, Dělnická, Tusarova, ...

## Instalace
* Vyžaduje python3, flask, flask-cache, BeautifulSoup, antiword, apache2, pdfplumber a nastavení z http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/
```shell
$ apt install python3 python3-pip antiword poppler-utils python3-opencv tesseract-ocr tesseract-ocr-ces # deb
```
```shell
$ pip3 install flask Flask-Cache beautifulsoup4 lxml Jinja2 Flask-Caching pdfplumber pytesseract
```
```shell
$ apt install libapache2-mod-wsgi
```

## Konfigurace
### Aplikace + spouštěcí wsgi soubor
```shell
cd /var/www/
git clone https://github.com/chinese-soup/zradlo.git
```
Ve složce /var/www/ vytvořit soubor wgsi, např. **jidelak.wgsi**
```python
import sys, os
#workaround
sys.path.insert(0,'/var/www/zradlo')
os.chdir("/var/www/zradlo")
from jidlo import app as application # import app
```

### Apache VirtualHost
Přidat VirtualHost do příslušného konfiguračního souboru (apache2.conf, httpd.conf, sites-available/něco.conf, conf.d/něco.conf, atd.)
```apache
<VirtualHost *:80>
    ServerName vase.domena.cz       

    WSGIDaemonProcess jidelak user=user1 group=group1 threads=5 # nastavit dle potreby!
    WSGIScriptAlias / /var/www/jidelak.wgsi # cesta k wgsi souboru
    WSGIScriptReloading On

    <Directory /var/www/zradlo>
        WSGIProcessGroup jidelak
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all

    </Directory>
</VirtualHost>

```
### Kdo radsi pouziva nginx
Do `/etc/uwsgi-emperor/vassals/zradlo.ini` neco takoveho:
```
[uwsgi]
base = /var/www/zradlo
chdir = %(base)
module = jidlo:app
home = %(base)/venv

socket = /run/zradlo/zradlo.sock
vacuum = true
chmod-socket    = 660

master = true
processes = 1
threads = 1

plugins = python3
logto = /var/log/zradlo/zradlo.log
```

A do virtualhostu:
```
server {
    listen      80;
    server_name vase.domena.cz;
    charset     utf-8;
    client_max_body_size 75M;

    location / { try_files $uri @zradlo; }
    location @zradlo {
        include uwsgi_params;
        uwsgi_pass unix:/run/zradlo/zradlo.sock;
    }
}
```
