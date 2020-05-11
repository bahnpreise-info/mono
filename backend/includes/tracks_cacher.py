#!/usr/bin/python
#encoding: utf-8

import datetime, time, json
from includes.functions import Logger, TrackPrices

# this class is responsible for agregating all track prices and sending them to the redis caching server
class TracksCacher():
    def __init__(self, db, redis):
        self.logger = Logger("TracksCacher")
        self.redis = redis
        self.db = db
        while True:
            self.logger.write("Start calculating tracks")
            for track in self.db.select("SELECT DISTINCT start, end FROM bahn_monitoring_connections"):
                self.cache(track)
            self.logger.write("Finished calculating tracks")
            time.sleep(600)

    def cache(self, track):
        self.logger.write("Processing {0} -> {1}".format(track["start"], track["end"]))
        trackdb = TrackPrices(self.db, track, self.redis)
        redis_cache = self.redis.get(trackdb.getRedisPath())
        if redis_cache is not None:
            self.logger.write("cache {0} already present".format(trackdb.getRedisPath()))
            return

        trackdb.getAggregatedData()
