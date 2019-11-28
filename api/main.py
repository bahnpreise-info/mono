#!/usr/bin/python
#encoding: utf-8

import time, falcon, json, datetime, redis
from configparser import ConfigParser
from orator import DatabaseManager
from datetime import timedelta

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
r = redis.Redis(host="redis")

class Bahnpricesforconnection:
    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
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
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        redis_cache = r.get("all_connections")
        if redis_cache is None:
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
            #Set redis cache
            r.setex("all_connections", timedelta(minutes=5), value=json.dumps(data))
        else:
            print("Using redis cache to serve request")
            data = json.loads(redis_cache)
        resp.body = json.dumps({"status": "success", "data": data})

class Getalltracks:
    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        redis_cache = r.get("all_tracks")
        if redis_cache is None:
            data = []
            query = "SELECT DISTINCT start, end FROM bahn_monitoring_connections"
            result = db.select(query)
            for track in result:
                data.append({
                    "start": track["start"],
                    "end": track["end"],
                })
            #Set redis cache
            r.setex("all_tracks", timedelta(minutes=5), value=json.dumps(data))
        else:
            print("Using redis cache to serve request")
            data = json.loads(redis_cache)
        resp.body = json.dumps({"status": "success", "data": data})

class Gettrackprice:
    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')

        #Gather start and end station from request parameters
        start = None
        end = None
        for key, value in req.params.items():
            if key == "start":
                start = value.encode('utf-8')
            if key == "end":
                end = value.encode('utf-8')
        if start is None or end is None:
            resp.body = json.dumps({"status": "error", "data": {}})
            return

        #The combination is possibly cached in redis
        cache="trackprice_{0}_{1}".format(start, end)
        redis_cache = r.get(cache)
        if redis_cache is not None:
            print("Using redis cache to serve request")
            resp.body = json.dumps({"status": "success", "data": json.loads(redis_cache)})
            return

        query = "SELECT \
            bahn_monitoring_connections.id, \
            bahn_monitoring_connections.start, \
            bahn_monitoring_connections.end, \
            bahn_monitoring_prices.price, \
            DATEDIFF(bahn_monitoring_connections.starttime, bahn_monitoring_prices.time) AS days_to_train_departure \
            FROM `bahn_monitoring_connections` \
            INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
            WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}'".format(start, end)
        result = db.select(query)

        days_with_prices = {}
        for price in result:
            current_days_to_train_departure = price["days_to_train_departure"]
            if not current_days_to_train_departure in days_with_prices:
                days_with_prices[current_days_to_train_departure] = []
            days_with_prices[current_days_to_train_departure].append(price["price"])

        threshold = 19
        minimum = 300.0
        maximum = 0.0
        for price in result:
            if float(price["price"]) < float(minimum) and float(price["price"]) > threshold:
                minimum = price["price"]
            if float(price["price"]) > float(maximum) and float(price["price"]) > threshold:
                maximum = price["price"]

        data = {"days_with_prices": {}, "minimum": minimum, "maximum": maximum}
        for day, prices in days_with_prices.iteritems():
            sum=0
            for price in prices:
                sum = sum + float(price)
            data["days_with_prices"][day] = round(sum / len(prices), 2)

        #Set redis cache for 30 minutes
        r.setex(cache, timedelta(minutes=30), value=json.dumps(data))
        resp.body = json.dumps({"status": "success", "data": data})

class Getrandomconnection:
    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        #Get random id
        query = "SELECT id FROM bahn_monitoring_connections WHERE active = 1 ORDER BY RAND() LIMIT 1"
        result = db.select(query)

        query = "SELECT bahn_monitoring_connections.id as connection_id, \
                bahn_monitoring_connections.start, \
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

        data = {"start": "", "end": "", "connection_id": "", "starttime": "", "prices_days_to_departure": {}}
        for price in result:
            data["start"] = price["start"]
            data["end"] = price["end"]
            data["connection_id"] = price["connection_id"]
            data["starttime"] = price["starttime"].strftime("%Y-%m-%d %H:%M:%S")
            data["prices_days_to_departure"].update({
                int(price["days_to_train_departure"]): float(price["price"])
            })
            resp.body = json.dumps({"status": "success", "data": data})

class Getstats:
    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        data = {"status": "success", "data": {}}

        redis_cache = r.get("stats_data")
        if redis_cache is None:
            data = {"status": "error_no_redis_data", "data": {}}
        else:
            print("Using redis cache to serve request")
            data["data"] = json.loads(redis_cache)
        resp.body = json.dumps(data)

class PricesXdaysbefore:
    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        days = 0
        for key, value in req.params.items():
            if key == "days":
                days = value

        if days is None or days == 0:
            resp.body = "Not enough info provided"
            return

        query = "SELECT ROUND(AVG(bahn_monitoring_prices.price), 2) as price \
        FROM bahn_monitoring_connections \
        INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
        WHERE DATEDIFF(bahn_monitoring_connections.starttime, bahn_monitoring_prices.time) = {0}".format(days)

        price = db.select(query)
        resp.body = json.dumps({"status": "success", "average": price[0]["price"]})


api = falcon.API()
api.add_route('/prices', Bahnpricesforconnection())
api.add_route('/stats', Getstats())
api.add_route('/stats/averageprices', PricesXdaysbefore())


api.add_route('/connections/getallconnections', Getallconnections())
api.add_route('/connections/getalltracks', Getalltracks())
api.add_route('/connections/getaveragetrackprice', Gettrackprice())
api.add_route('/connections/getrandomconnection', Getrandomconnection())


