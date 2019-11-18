from includes import mysql
import datetime, configparser, logging, time, pytz, redis, json
from orator import DatabaseManager

#os.chdir("/opt/app") #change this according to your needs - working directory

config = configparser.ConfigParser()
config.read_file(open('database.ini'))
oratorconfig = {
    'scheduler': {
        'driver': 'mysql',
        'host':  config.get('database', 'host'),
        'database': config.get('database', 'database'),
        'user': config.get('database', 'user'),
        'password': config.get('database', 'password'),
        'prefix': config.get('database', 'database_prefix'),
    }
}
db = DatabaseManager(oratorconfig)
r = redis.Redis(host="redis")

class StatisticsCalculator():
    def __init__(self):
        self.status = {}    #saves the status (true/false) of important jobs
        self.status['logger'] = self.setupLogger()
        self.local = pytz.timezone("Europe/Berlin")
        if self.status['logger']:
            self.logger.debug("logger setup successfull")
        else:
            print("FATAL ERROR: Could not setup a logger. Stopped execution.")
        if self.status['logger']:
            while True:
                self.logger.info("Start gathering logs")
                self.calculate()
                self.logger.info("Finished gathering logs")
                time.sleep(60)

    def setupLogger(self):
        try:
            self.logger = logging.getLogger('Scheduler')
            self.logger.setLevel(logging.INFO)
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

    def calculate(self):
        data={}
        self.logger.debug("Getting stats from database")
        self.logger.debug("Getting Requests in past hour")
        query = "SELECT * FROM bahn_monitoring_prices WHERE bahn_monitoring_prices.time >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
        result = db.select(query)
        data["hourlyrequests"] = len(result)

        self.logger.debug("Getting Requests within the last day")
        query = "SELECT * FROM bahn_monitoring_prices WHERE bahn_monitoring_prices.time >= DATE_SUB(NOW(), INTERVAL 1 DAY)"
        result = db.select(query)
        data["dailyrequests"] = len(result)

        self.logger.debug("Getting station count")
        query = "SELECT * FROM bahn_monitoring_stations"
        result = db.select(query)
        data["stationcount"] = len(result)

        self.logger.debug("Getting connection count")
        query = "SELECT * FROM bahn_monitoring_connections"
        result = db.select(query)
        data["connections"] = len(result)

        self.logger.debug("Getting active connection count")
        query = "SELECT * FROM bahn_monitoring_connections WHERE active = 1"
        result = db.select(query)
        data["activeconnections"] = len(result)

        self.logger.debug("Getting average price")
        query = "SELECT ROUND(AVG(bahn_monitoring_prices.price), 2) as average FROM bahn_monitoring_connections INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id)"
        result = db.select(query)
        data["globalaverageprice"] = result[0]["average"]

        self.logger.debug("Getting minimum and maximum prices for each days before departure")
        days_to_prices = {}
        days_to_minimum_prices = {}
        days_to_maximum_prices = {}
        query = "SELECT bahn_monitoring_prices.price, DATEDIFF(bahn_monitoring_connections.starttime, bahn_monitoring_prices.time) AS days_to_train_departure FROM bahn_monitoring_prices INNER JOIN bahn_monitoring_connections ON (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) WHERE bahn_monitoring_prices.price > 0"
        result = db.select(query)
        for price in result:
            if not price["days_to_train_departure"] in days_to_prices:
                days_to_prices[price["days_to_train_departure"]] = []
            days_to_prices[price["days_to_train_departure"]].append(price["price"])

        for day, prices in days_to_prices.items():
            threshold = 19
            minimum = 300.0
            maximum = 0.0
            for price in prices:
                if float(price) < float(minimum) and float(price) > threshold:
                    minimum = price
                if float(price) > float(maximum) and float(price) > threshold:
                    maximum = price
            days_to_minimum_prices[day] = minimum
            days_to_maximum_prices[day] = maximum
        data["days_to_average_prices"] = {}
        data["days_to_average_prices"]["minimum"] = days_to_minimum_prices
        data["days_to_average_prices"]["maximum"] = days_to_maximum_prices

        self.logger.debug("Getting average price per weekday")
        data["prices_to_weekdays"] = {}
        data["prices_to_weekdays_stdev"] = {}
        map = {0 : "monday", 1 : "tuesday", 2 : "wednesday", 3 : "thursday", 4 : "friday", 5 : "saturday", 6 : "sunday"}
        query = "SELECT ROUND(AVG(bahn_monitoring_prices.price), 2) as average, WEEKDAY(bahn_monitoring_prices.time) AS weekday from bahn_monitoring_prices GROUP by weekday"
        results = db.select(query)
        for result in results:
            data["prices_to_weekdays"][map[result["weekday"]]] = result["average"]

        self.logger.debug("Getting  standard deviation price per weekday")
        query = "SELECT ROUND(STD(bahn_monitoring_prices.price), 2) as average, WEEKDAY(bahn_monitoring_prices.time) AS weekday from bahn_monitoring_prices GROUP by weekday"
        results = db.select(query)
        for result in results:
            data["prices_to_weekdays_stdev"][map[result["weekday"]]] = result["average"]


        r.setex("stats_data", datetime.timedelta(minutes=5), value=json.dumps(data))
