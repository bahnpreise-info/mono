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
class TracksCacher():
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
                try:
                    self.logger.info("Start calculating tracks")
                    self.cachetracks()
                    self.logger.info("Finished calculating tracks")
                    time.sleep(60)
                except:
                    time.sleep(5)
    # setup a logger
    def setupLogger(self):
        try:
            self.logger = logging.getLogger('TracksCalculator')
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

    def cachetracks(self):
        query = "SELECT DISTINCT start, end FROM bahn_monitoring_connections"
        tracks = db.select(query)
        for track in tracks:
            try:
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
            except:
                self.logger.debug("Error while processing connection {0} -> {1}".format(track["start"], track["end"]))
