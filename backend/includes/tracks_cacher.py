#!/usr/bin/python
#encoding: utf-8

import datetime, logging, time, pytz, json, math
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
                self.cachetracks(track)
            self.logger.write("Finished calculating tracks")
            time.sleep(600)

    def cachetracks(self, track):
        self.logger.write("Processing {0} -> {1}".format(track["start"], track["end"]))

        #The combination is possibly cached in redis
        cache="trackprice_{0}_{1}".format(track["start"], track["end"]).replace(" ", "_")
        redis_cache = self.redis.get(cache)
        if redis_cache is not None:
            self.logger.write("cache {0} already present".format(cache))
            return

        trackdb = TrackPrices(self.db, track)
        data = {"days_with_prices": trackdb.dailyaverage(), "minimum": trackdb.minimum(), "maximum": trackdb.maximum(), "average": trackdb.average(), "datapoints": trackdb.datapoints(), "maximumpricejump_up": trackdb.maxjumpup(),  "maximumpricejump_down": trackdb.maxjumpdown()}

        #Set redis cache for 30 minutes
        self.redis.setex(cache, datetime.timedelta(minutes=30), value=json.dumps(data))