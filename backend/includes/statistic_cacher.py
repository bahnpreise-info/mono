#!/usr/bin/python
#encoding: utf-8

import datetime, time, json
from includes.functions import Logger, Statistics

# this class is responsible for calculating all the statistics and sending them to the redis caching server
class StatisticsCalculator():
    def __init__(self, db, redis):
        self.db = db
        self.redis = redis
        self.logger = Logger("StatisticsCacher")
        while True:
            self.logger.write("Start calculating statistics")
            self.cache()
            self.logger.write("Finished calculating statistics")
            time.sleep(60)
    # calculate the statistics
    def cache(self):
        cache = "stats_data"
        redis_cache = self.redis.get(cache)
        if redis_cache is not None:
            self.logger.write("cache {0} already present".format(cache))
            return

        statisticsdb = Statistics(self.db)
        data = {
            "prices_to_weekdays": statisticsdb.prices_to_weekdays(),
            "lowest_price_per_weekday": statisticsdb.lowest_price_per_weekday(),
            "highest_price_per_weekday": statisticsdb.highest_price_per_weekday(),
            "global_average": statisticsdb.global_average(),
            "connections": statisticsdb.connections(),
            "activeconnections": statisticsdb.activeconnections(),
            "stationcount": statisticsdb.stationcount(),
            "hourlyrequests": statisticsdb.hourlyrequests(),
            "dailyrequests": statisticsdb.dailyrequests()
        }
        self.logger.write(data)
        #send everything to the redis cache, so the api can access it
        self.redis.setex(cache, datetime.timedelta(minutes=15), value=json.dumps(data))
