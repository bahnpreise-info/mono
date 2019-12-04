#!/usr/bin/python
#encoding: utf-8

import datetime, logging, time, pytz, redis, json, math
from orator import DatabaseManager
from configparser import ConfigParser

#this line is not needed anymore i think
#os.chdir("/opt/app") #change this according to your needs - working directory

# setup database connection, read from config file
config = ConfigParser()
config.read_file(open('database.ini'))
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
r = redis.Redis(host=config.get('redis', 'host'))

# this class is responsible for calculating all the statistics and sending them to the redis caching server
class StatisticsCalculator():
    def __init__(self):
        self.status = {} #saves the status (true/false) of important jobs
        self.status['logger'] = self.setupLogger()
        self.local = pytz.timezone("Europe/Berlin")
        if self.status['logger']:
            self.logger.debug("logger setup successfull")
        else:
            print("FATAL ERROR: Could not setup a logger. Stopped execution.")
        if self.status['logger']:
            while True:
                self.logger.info("Start calculating statistics")
                self.cachestats()
                self.cachetracks()
                self.logger.info("Finished calculating statistics")
                time.sleep(60)
    # setup a logger
    def setupLogger(self):
        try:
            self.logger = logging.getLogger('StatisticsCalculator')
            self.logger.setLevel(logging.DEBUG)
            self.ch = logging.StreamHandler()
            self.ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.ch.setFormatter(formatter)
            self.logger.addHandler(self.ch)
            self.logger.debug("--------------------------------- START --------------------------------")
            self.logger.debug("Successfuly setup the logger.")
            return True
        except Exception as e:
            print(e)
            return False

    # calculate the statistics
    def cachestats(self):
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
        r.setex("stats_data", datetime.timedelta(minutes=5), value=json.dumps(data))

    def cachetracks(self):
        query = "SELECT DISTINCT start, end FROM bahn_monitoring_connections"
        tracks = db.select(query)
        for track in tracks:
            #Cast to utf-8
            start = track["start"]
            end = track["end"]

            #Log something
            self.logger.debug("Processing {0} -> {1}".format(start, end))

            #The combination is possibly cached in redis
            cache="trackprice_{0}_{1}".format(start, end).replace(" ", "_")
            redis_cache = r.get(cache)
            if redis_cache is not None:
                self.logger.debug("cache {0} already present".format(cache))
                continue

            query = "SELECT \
                bahn_monitoring_connections.id, \
                bahn_monitoring_connections.start, \
                bahn_monitoring_connections.end, \
                bahn_monitoring_prices.price, \
                bahn_monitoring_prices.time, \
                DATEDIFF(bahn_monitoring_connections.starttime, bahn_monitoring_prices.time) AS days_to_train_departure \
                FROM bahn_monitoring_connections \
                INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
                WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}' \
                ORDER BY bahn_monitoring_prices.time ASC".format(track["start"], track["end"])
            result = db.select(query)

            if result is None:
                 continue
            if len(result) == 0:
                continue

            threshold = 15.0
            minimum = 300.0
            maximum = 0.0
            sum_prices = 0
            days_with_prices = {}
            for price in result:
                if float(price["price"]) == float(0):
                    continue
                current_days_to_train_departure = price["days_to_train_departure"]
                if not current_days_to_train_departure in days_with_prices:
                    days_with_prices[current_days_to_train_departure] = []
                days_with_prices[current_days_to_train_departure].append(price["price"])

                if float(price["price"]) < float(minimum) and float(price["price"]) > threshold:
                    minimum = price["price"]
                if float(price["price"]) > float(maximum) and float(price["price"]) > threshold:
                    maximum = price["price"]
                sum_prices = sum_prices + float(price["price"])

            lastprice = 0.0
            maximumpricejump_up = 0.0
            _days_with_prices = {}
            for day, prices in days_with_prices.items():
                sum=0
                for price in prices:
                    sum = sum + float(price)
                avg_price_for_day = round(sum / len(prices), 2)
                _days_with_prices[day] = avg_price_for_day

                if lastprice == 0.0:
                    lastprice = avg_price_for_day
                    continue
                if avg_price_for_day > lastprice and avg_price_for_day - lastprice > maximumpricejump_up:
                    maximumpricejump_up = avg_price_for_day - lastprice
                lastprice = avg_price_for_day

            data = {"days_with_prices": _days_with_prices, "minimum": float(minimum), "maximum": float(maximum), "average": float(round(sum_prices / len(result), 2)), "datapoints": len(result), "maximumpricejump_up": round(float(maximumpricejump_up), 2)}

            #Set redis cache for 30 minutes
            r.setex(cache, datetime.timedelta(minutes=30), value=json.dumps(data))
