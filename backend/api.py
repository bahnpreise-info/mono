#!/usr/bin/python
#encoding: utf-8

from includes.functions import Logger, TrackPrices,ConnectionPrices
import time, falcon, json, datetime, redis
from configparser import ConfigParser
from orator import DatabaseManager
from datetime import timedelta
from falcon_prometheus import PrometheusMiddleware

#Read mysql config
config = ConfigParser()
config.readfp(open('database.ini'))

oratorconfig = {
    'scheduler': {
        'driver': 'mysql',
        'host': config.get('database', 'host'),
        'database': config.get('database', 'database'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'prefix': ''
    }
}
db = DatabaseManager(oratorconfig)
db.connection().enable_query_log()
r = redis.Redis(host=config.get('redis', 'host'))

class Bahnpricesforconnection:
    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')
        id = 0
        for key, value in req.params.items():
            if key == "connection_id":
                id = value

        #return error in case we did not receive any connection id
        if id is None or id is 0:
            resp.body = json.dumps({"status": "error", "data": {}, "msg": "Not enough info provided"})
            return

        #Initialize ConnectionPrices Class to gather some info from
        connectiondb = ConnectionPrices(db, id, r)

        #The connection may be already cached
        redis_cache = r.get(connectiondb.getRedisPath())
        if redis_cache is not None:
            data = json.loads(redis_cache)
        else:
           data = connectiondb.getAggregatedData()

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
            resp.body = json.dumps({"status": "error", "data": {"message": "Please specify 'start' and 'end' station as request parameter"}})
            return

        #Initialize TrackPrices Class to gather some info from
        trackdb = TrackPrices(db, {"start": start.decode('utf-8'), "end": end.decode(('utf-8'))}, redis)

        #The connection may be already cached
        redis_cache = r.get(trackdb.getRedisPath())
        if redis_cache is not None:
            data = json.loads(redis_cache)
        else:
            data = trackdb.getAggregatedData()

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

prometheus = PrometheusMiddleware()
api = falcon.API(middleware=prometheus)
api.add_route('/metrics', prometheus)
api.add_route('/prices', Bahnpricesforconnection()) #todo refactor to /connections/getaverageconnectionprice
api.add_route('/stats', Getstats())


api.add_route('/connections/getallconnections', Getallconnections())
api.add_route('/connections/getaverageconnectionprice', Bahnpricesforconnection()) #todo refactor to funktion
api.add_route('/connections/getalltracks', Getalltracks())
api.add_route('/connections/getaveragetrackprice', Gettrackprice())
api.add_route('/connections/getrandomconnection', Getrandomconnection())


