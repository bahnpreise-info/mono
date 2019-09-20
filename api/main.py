#!/usr/bin/python
import time, falcon, json, datetime, redis
from configparser import ConfigParser
from orator import DatabaseManager

#Read mysql config
mysqlconfig = ConfigParser()
mysqlconfig.readfp(open('config/mysql.ini'))

oratorconfig = {
    'scheduler': {
        'driver': 'mysql',
        'host': mysqlconfig.get('sheduler', 'host'),
        'database': mysqlconfig.get('sheduler', 'database'),
        'user': mysqlconfig.get('sheduler', 'username'),
        'password': mysqlconfig.get('sheduler', 'password'),
        'prefix': ''
    }
}
db = DatabaseManager(oratorconfig)
db.connection().enable_query_log()
r = redis.Redis(host='redis_db', port=6379, db=0)

class Bahnpricesforconnection:
    def on_get(self, req, resp):
        id = 0
        for key, value in req.params.items():
            if key == "connection_id":
                id = value

        if id == None or id == 0:
            resp.body = "Not enough info provided"
            return

        query = "SELECT bahn_monitoring_connections.start, \
        bahn_monitoring_connections.end, \
        bahn_monitoring_connections.starttime, \
        bahn_monitoring_prices.time as querytime, \
        bahn_monitoring_prices.price, \
        DATEDIFF(bahn_monitoring_connections.starttime, bahn_monitoring_prices.time) AS days_to_train_departure \
        FROM bahn_monitoring_connections \
        INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
        WHERE price > 0 AND \
        bahn_monitoring_connections.id = {0} \
        HAVING days_to_train_departure IN (1,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,69,70,71,79,80,81,89,90,91,99,100,101,109,110,111,119,120,121,129,130,131,139,140,141)".format(id)
        database_prices = db.select(query)

        data = {"start": "", "end": "", "starttime": "", "prices_days_to_departure": {}}

        for price in database_prices:
            data["start"] = price["start"]
            data["end"] = price["end"]
            data["starttime"] = price["starttime"].strftime("%Y-%m-%d %H:%M:%S")
            data["prices_days_to_departure"].update({
                int(price["days_to_train_departure"]): float(price["price"])
            })
        resp.body = json.dumps({"status": "success", "data": data})


class Getallconnections:
    def on_get(self, req, resp):
        cache = r.get('all_connections')
        if cache is not None:
            cache = json.loads(cache)
            resp.body = json.dumps({"status": "success", "data": cache})
        data = []
        database_connections = db.table('bahn_monitoring_connections').get()
        for connection in database_connections:
            data.append({
                "connection_id": connection["id"],
                "start": connection["start"],
                "end": connection["end"],
                "starttime": connection["starttime"].strftime("%Y-%m-%d %H:%M:%S"),
                "endtime": connection["endtime"].strftime("%Y-%m-%d %H:%M:%S"),
            })
        r.set('all_connections', json.dumps(data))
        r.expire('all_connections', 60)
        resp.body = json.dumps({"status": "success", "data": data})

class Getrandomconnection:
    def on_get(self, req, resp):
        #Get random id
        query = "SELECT id FROM bahn_monitoring_connections WHERE active = 1 ORDER BY RAND() LIMIT 1"
        result = db.select(query)

        query = "SELECT bahn_monitoring_connections.start, \
        bahn_monitoring_connections.end, \
        bahn_monitoring_connections.starttime, \
        bahn_monitoring_prices.time as querytime, \
        bahn_monitoring_prices.price, \
        DATEDIFF(bahn_monitoring_connections.starttime, bahn_monitoring_prices.time) AS days_to_train_departure \
        FROM bahn_monitoring_connections \
        INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
        WHERE bahn_monitoring_connections.id = {0} \
        HAVING days_to_train_departure IN (1,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,69,70,71,79,80,81,89,90,91,99,100,101,109,110,111,119,120,121,129,130,131,139,140,141)".format(result[0]["id"])
        result = db.select(query)

        data = {"start": "", "end": "", "starttime": "", "prices_days_to_departure": {}}
        for price in result:
            data["start"] = price["start"]
            data["end"] = price["end"]
            data["starttime"] = price["starttime"].strftime("%Y-%m-%d %H:%M:%S")
            data["prices_days_to_departure"].update({
                int(price["days_to_train_departure"]): float(price["price"])
            })
            resp.body = json.dumps({"status": "success", "data": data})

class Getstats:
    def on_get(self, req, resp):

        cache = r.get('statistics')
        if cache is not None:
            cache = json.loads(cache)
            resp.body = json.dumps({"status": "success", "data": cache})

        data = {"status": "success", "data": {}}
        # Requests in past hour
        query = "SELECT * FROM bahn_monitoring_prices WHERE bahn_monitoring_prices.time >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
        result = db.select(query)
        data["data"]["hourlyrequests"] = len(result)

        #Requests within the last day
        query = "SELECT * FROM bahn_monitoring_prices WHERE bahn_monitoring_prices.time >= DATE_SUB(NOW(), INTERVAL 1 DAY)"
        result = db.select(query)
        data["data"]["dailyrequests"] = len(result)

        #Get station count
        query = "SELECT * FROM bahn_monitoring_stations"
        result = db.select(query)
        data["data"]["stationcount"] = len(result)

        #Get connection count
        query = "SELECT * FROM bahn_monitoring_connections"
        result = db.select(query)
        data["data"]["connections"] = len(result)

        #Get active connection count
        query = "SELECT * FROM bahn_monitoring_connections WHERE active = 1"
        result = db.select(query)
        data["data"]["activeconnections"] = len(result)

        #Get average price
        query = "SELECT ROUND(AVG(bahn_monitoring_prices.price), 2) as average FROM bahn_monitoring_connections INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id)"
        result = db.select(query)
        data["data"]["globalaverageprice"] = result[0]["average"]

        r.set('statistics', json.dumps(data["data"]))
        r.expire('statistics', 60)
        resp.body = json.dumps(data)

api = falcon.API()
api.add_route('/prices', Bahnpricesforconnection())

api.add_route('/connections/getallconnections', Getallconnections())
api.add_route('/connections/getrandomconnection', Getrandomconnection())

api.add_route('/stats', Getstats())
