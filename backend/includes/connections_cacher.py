#!/usr/bin/python
#encoding: utf-8

import datetime, time, json
from includes.functions import Logger, ConnectionPrices

# this class is responsible for agregating all connection prices and sending them to the redis caching server
class ConnectionsCacher():
    def __init__(self, db, redis):
        self.logger = Logger("ConnectionsCacher")
        self.redis = redis
        self.db = db
        while True:
            self.logger.write("Start caching aggregated connection prices")
            for connection in self.db.select("SELECT * FROM bahn_monitoring_connections"):
                self.cache(connection)
            self.logger.write("Finished caching aggregated connection prices")
            time.sleep(600)

    def cache(self, connection):
        self.logger.write("Processing {0} -> {1} @ {2}".format(connection["start"], connection["end"], connection["starttime"]))

        #The connection may be already cached
        cache="connection_{0}".format(connection["id"])
        redis_cache = self.redis.get(cache)
        if redis_cache is not None:
            self.logger.write("cache {0} already present".format(cache))
            return

        connectiondb = ConnectionPrices(self.db, connection)
        data = {"days_with_prices": connectiondb.dailyaverage(), "minimum": connectiondb.minimum(), "maximum": connectiondb.maximum(), "average": connectiondb.average(), "datapoints": connectiondb.datapoints(), "maximumpricejump_up": connectiondb.maxjumpup(),  "maximumpricejump_down": connectiondb.maxjumpdown()}

        #Set redis cache for 6 hours
        self.redis.setex(cache, datetime.timedelta(hours=6), value=json.dumps(data))