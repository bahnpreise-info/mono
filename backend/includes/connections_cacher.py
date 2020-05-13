#!/usr/bin/python
#encoding: utf-8

import datetime, time, json
from includes.functions import Logger, ConnectionPrices, Offset

# this class is responsible for agregating all connection prices and sending them to the redis caching server
class ConnectionsCacher():
    def __init__(self, db, redis):
        self.offset = Offset()
        self.logger = Logger("ConnectionsCacher")
        self.redis = redis
        self.db = db
        while True:
            try:
                self.logger.write("Start caching aggregated connection prices")
                for connection in self.db.select("SELECT * FROM bahn_monitoring_connections where active = 1"):
                    self.cache(connection, self.offset)
                self.logger.write("Finished caching aggregated connection prices")
                time.sleep(600)
            except:
                time.sleep(10)

    def cache(self, connection, offset):
        self.logger.write("Processing {0} -> {1} @ {2}".format(connection["start"], connection["end"], connection["starttime"]))
        connectiondb = ConnectionPrices(self.db, connection["id"], self.redis)

        #The connection may be already cached
        cache=connectiondb.getRedisPath()
        connectiondb.getAggregatedData() #we don't do anything, but the function refreshed the cache