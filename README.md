# Bahnpreise.info

**Beta-Version**

Bahnpreise.info ist ein Tool, dass die Entwicklung von Ticketpreisen des Bahnverkehrs beobachtet und grafisch aufbereitet.

Unter [www.bahnpreise.info](https://bahnpreise.info) ist die Instanz der Entwickler [storedcc](https://stored.cc) und [cubicrootxyz](https://cubicroot.xyz) nutzbar.

## Kompatibel
* Deutsche Bahn (Spar- /Flexpreise, 2. Klasse)

## Aufbau
### Backend
Das Backend sammelt die Daten und managed die Verbindungen. Geschrieben in Python.
### API
Die JSON-API stellt die Informationen des Backends zur Verfügung. Geschrieben in Python.
### Frontend
Das Frontend ist eine Website, geschrieben in JavaScript, sie stellt die Daten der API graphisch dar.

## Installation (English)
### Backend
**Prerequisites**

You need a MySQL-Server with a single database for this tool.
You need Python 3 installed.

**Installation**

1. Download the backend-folder.
2. Add all the database-credentials to the `connectionmanager.ini` and `scheduler.ini`.
3. IMPORTANT: change the working directory in the `scheduler.py` and the `connectionmanager.py` to the current folder where the files are.
4. Run the `connectionmanager.py` once, that will create all the needed tables, do not regard the errors ^^. Make sure to use Python 3.
5. Insert stations into the table `bahn_monitoring_stations`. You just need to fill in the name, use the station name (e.g. "Berlin Hbf"). Do not use stations that are to far away from each other (more than one day driving time), else there might be some displaying errors.
6. Let the `connectionmanager.py` run every few minutes/hours (e.g. make a cronjob each 10 minutes). In the last line change the number in run = ConnectionManager(10), this number is the maximum of connections that are monitored.
7. Let the `scheduler.py` run very few minutes (e.g. every 3 minutes). Or rewrite it as a daemon.

Thats it, now the database should fill up with connections and prices.

### Frontend
In the frontend folder you will find a simple HTML/Javascript only application which can be thrown on basically every webserver out there. No php/external ressources needed.

### API
In the `api` folder you will find a python/falcon application which needs the following packages installed via apt / pip:
```
apt-get update && apt-get install python python-pip python-mysqldb -y
pip install gunicorn falcon orator
```

Also, the API needs to connect to the same database as the sheduler backend. You should have the mysql database set up at this point, so you can simply instert the host/username/database/password into the `mysql.ini` config file in the config folder.

After that, the api can be started with the command provided in the startapi.sh:
`gunicorn --workers 4 -b 0.0.0.0:8080 main:api -b [::1]:8080 --reload`

## Externe Ressourcen
* [Schiene Bibliothek](https://github.com/kennell/schiene) von Kennell
* [Bootstrap](http://getbootstrap.com)
* [SB Admin 2 Theme](https://github.com/BlackrockDigital/startbootstrap-sb-admin-2)

## Bekannte Probleme
**Verbindungen > 24 Stunden werden nicht korrekt angezeigt**

Die genutzte Bibliothek zum parsen der Preise erkennt leider keine Tage, sondern nur Stunden. Daher kann es zu Anzeigefehlern kommen, wenn Verbindungen über einen Tag hinaus gehen.

**Viele "Could not create Connection" Errors**

Das liegt daran, dass öfters keine Verbindung zu den gegebenen Rahmendaten (Start, Ziel, Uhrzeit) gefunden werden. Einfach ignorieren, das Tool sucht dann einfach nach einer neuen Verbindung.

**Große Preissprünge auf kurzer Zeit**

Das kann unter anderem daran liegen, dass interne APIs der Bahnbetreiber nicht erreichbar sind. Bei der DB z.B. die Sparpreise-API, dann werden nur die teureren Flex-Preise angezeigt. 
