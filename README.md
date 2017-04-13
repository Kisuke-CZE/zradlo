# Zradlo
### Stránka pro agregaci jídelníčku poblíž ulic Argentinská, Dělnická, Tusarova, ...

## Instalace
* Vyžaduje python3, flask, flask-cache, BeautifulSoup, apache2 a nastavení z http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/
```shell
$ apt-get install python3 python3-pip # deb
```
```shell
$ pip3 install flask Flask-Cache beautifulsoup4 lxml Jinja2
```
```shell
$ apt-get install libapache2-mod-wsgi
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
    ServerName jidlo.o2its.cz
    ServerAlias jidlo.memer.top       

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


