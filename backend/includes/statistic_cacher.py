#!/usr/bin/python
#encoding: utf-8

import datetime, logging, time, json, math

# this class is responsible for calculating all the statistics and sending them to the redis caching server
class StatisticsCalculator(db, redis):
    def __init__(self):
        self.db = db
        self.redis = redis
        while True:
            try:
                self.logger.write("Start calculating statistics")
                self.cachestats()
                self.logger.write("Finished calculating statistics")
                time.sleep(60)
            except:
                time.sleep(5)

    # calculate the statistics
    def cachestats(self):
        #todo: refactor to functions.py
        data={}
        self.logger.debug("Getting stats from database")

        # get amount of prices from the last hour
        self.logger.debug("Getting Requests from past hour")
        query = "SELECT * FROM bahn_monitoring_prices WHERE bahn_monitoring_prices.time >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
        result = db.select(query)
        data["hourlyrequests"] = len(result)

        # get amount of prices from the last 24 hours
        self.logger.debug("Getting Requests within the last day")
        query = "SELECT * FROM bahn_monitoring_prices WHERE bahn_monitoring_prices.time >= DATE_SUB(NOW(), INTERVAL 1 DAY)"
        result = db.select(query)
        data["dailyrequests"] = len(result)

        # get the amount of stations available
        self.logger.debug("Getting station count")
        query = "SELECT * FROM bahn_monitoring_stations"
        result = db.select(query)
        data["stationcount"] = len(result)

        # get amount of all connections from the database
        self.logger.debug("Getting connection count")
        query = "SELECT * FROM bahn_monitoring_connections"
        result = db.select(query)
        data["connections"] = len(result)

        # get amount of all active monitored connections
        self.logger.debug("Getting active connection count")
        query = "SELECT * FROM bahn_monitoring_connections WHERE active = 1"
        result = db.select(query)
        data["activeconnections"] = len(result)

        # get average price from all connections
        self.logger.debug("Getting average price")
        query = "SELECT ROUND(AVG(bahn_monitoring_prices.price), 2) as average FROM bahn_monitoring_connections INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id)"
        result = db.select(query)
        data["globalaverageprice"] = result[0]["average"]

        # calculate statistics by days to departure
        self.logger.debug("Getting minimum and maximum prices for each days before departure")
        days_to_prices = {}
        # these dicts holds one statistical value for each day
        days_to_minimum_prices = {}
        days_to_maximum_prices = {}
        days_to_average_prices = {}
        days_to_deviation_prices = {}
        query = "SELECT bahn_monitoring_prices.price, DATEDIFF(bahn_monitoring_connections.starttime, bahn_monitoring_prices.time) AS days_to_train_departure FROM bahn_monitoring_prices INNER JOIN bahn_monitoring_connections ON (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) WHERE bahn_monitoring_prices.price > 0"
        result = db.select(query)
        for price in result:
            if not price["days_to_train_departure"] in days_to_prices:
                days_to_prices[price["days_to_train_departure"]] = []
            days_to_prices[price["days_to_train_departure"]].append(price["price"])

        for day, prices in days_to_prices.items():

            # calc statistics by day
            threshold = 19
            minimum = 300.0
            maximum = 0.0
            sum_ = 0
            i = 0
            for price in prices:
                i += 1
                sum_ += float(price)
                if float(price) < float(minimum) and float(price) > threshold:  # minimum daily price
                    minimum = price
                if float(price) > float(maximum) and float(price) > threshold:  # maximum daily price
                    maximum = price
            days_to_minimum_prices[day] = minimum
            days_to_maximum_prices[day] = maximum
            days_to_average_prices[day] = round(sum_/i, 2)  # average daily price

            stdDev = 0
            i = 0
            for price in prices:
                i += 1
                stdDev += math.pow(days_to_average_prices[day]-float(price), 2) # deviation for each day
            days_to_deviation_prices[day] = round(math.sqrt(stdDev/i), 2)

        data["days_to_average_prices"] = {}
        data["days_to_minimum_prices"] = days_to_minimum_prices
        data["days_to_maximum_prices"] = days_to_maximum_prices
        data["days_to_average_prices"] = days_to_average_prices
        data["days_to_deviation_prices"] = days_to_deviation_prices

        # calculate statistics by weekday (0-6 => Monday-Sunday)
        self.logger.debug("Getting average price per weekday")

        data["prices_to_weekdays"] = {}
        data["prices_to_weekdays_stdev"] = {}
        map = {0 : "monday", 1 : "tuesday", 2 : "wednesday", 3 : "thursday", 4 : "friday", 5 : "saturday", 6 : "sunday"}
        query = "SELECT ROUND(AVG(bahn_monitoring_prices.price), 2) as average, WEEKDAY(bahn_monitoring_prices.time) AS weekday from bahn_monitoring_prices GROUP by weekday"
        results = db.select(query)
        for result in results:
            data["prices_to_weekdays"][map[result["weekday"]]] = result["average"]  # average price by weekday

        self.logger.debug("Getting  standard deviation price per weekday")
        query = "SELECT ROUND(STD(bahn_monitoring_prices.price), 2) as average, WEEKDAY(bahn_monitoring_prices.time) AS weekday from bahn_monitoring_prices GROUP by weekday"
        results = db.select(query)
        for result in results:
            data["prices_to_weekdays_stdev"][map[result["weekday"]]] = result["average"]    # deviation by weekday

        # send everything to the redis cache, so the api can access it
        self.redis.setex("stats_data", datetime.timedelta(minutes=15), value=json.dumps(data))
