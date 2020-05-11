import time, datetime, json

class Logger:
    def __init__(self, prefix):
        self.verbose = True
        self.prefix = prefix
        self.message = ""

    def getFormattedOutput(self):
        return "[%s] [%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S" ,time.gmtime()), self.prefix, self.message)

    def write(self, message):
        self.message = str(message)
        print(self.getFormattedOutput())

class TrackPrices:
    def __init__(self, connection, track, redis):
        self.offset = 130
        self.connection = connection
        self.track = track
        self.redis = redis

    def float(self, value):
        return round(float(value), 2)

    def int(self, value):
        return int(value)

    def datapoints(self):
        #Get count of datapoints collected for this track
        query = "SELECT \
                        COUNT(bahn_monitoring_prices.id) as count \
                        FROM bahn_monitoring_prices \
                        INNER JOIN bahn_monitoring_connections on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
                        WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}' \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {2} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0".format(self.track["start"], self.track["end"], self.offset)

        result = self.connection.select(query)
        if result is not None and result[0]["count"] is not None:
            return self.int(result[0]["count"])

    def average(self):
        #Get overall average for this track
        query = "SELECT \
                        ROUND(avg(bahn_monitoring_prices.price), 2) as average_price, \
                        DATEDIFF(bahn_monitoring_connections.starttime, bahn_monitoring_prices.time) AS days_to_train_departure \
                        FROM bahn_monitoring_connections \
                        INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
                        WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}' \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {2} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0".format(self.track["start"], self.track["end"], self.offset)
        result = self.connection.select(query)
        if result is not None and result[0]["average_price"] is not None:
            return self.float(result[0]["average_price"])

    def dailyaverage(self):
        #Get average prices grouped by days until the train departs (days_to_train_departure)
        query = "SELECT \
                        ROUND(avg(bahn_monitoring_prices.price), 2) as average_price, \
                        DATEDIFF(bahn_monitoring_connections.starttime, bahn_monitoring_prices.time) AS days_to_train_departure \
                        FROM bahn_monitoring_connections \
                        INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
                        WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}' \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {2} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0 \
                        GROUP BY days_to_train_departure \
                        ORDER BY bahn_monitoring_prices.time ASC".format(self.track["start"], self.track["end"], self.offset)
        _days_with_prices = {}
        for row in self.connection.select(query):
            _days_with_prices[row["days_to_train_departure"]] = row["average_price"]
        return _days_with_prices

    def maxjumpup(self):
        max=0.0
        last=0.0
        for days_to_train_departure, price in self.dailyaverage().items():
            if last == 0.0:
                last = price
                max = price
                continue
            if price > last and price - last > max:
                max = price - last
        return self.float(max)

    def maxjumpdown(self):
        max=0.0
        last=0.0
        for days_to_train_departure, price in self.dailyaverage().items():
            if last == 0.0:
                last = price
                max = price
                continue
            if price < last and last - price > max:
                max = last -price
        return self.float(max)

    def maximum(self):
        maximum = 0.0
        query = "SELECT \
                        MAX(DISTINCT bahn_monitoring_prices.price) as maximum \
                        FROM bahn_monitoring_prices \
                        INNER JOIN bahn_monitoring_connections on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
                        WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}' \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {2} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0".format(self.track["start"], self.track["end"], self.offset)
        result = self.connection.select(query)
        if result is not None and result[0]["maximum"] is not None:
            maximum = result[0]["maximum"]

        #Hacky workarround, mysql MAX function does not return values over 99.0 when > 100 is not given. Wtf.
        #Query again for values > 100
        query = "SELECT \
                        MAX(DISTINCT bahn_monitoring_prices.price) as maximum \
                        FROM bahn_monitoring_prices \
                        INNER JOIN bahn_monitoring_connections on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
                        WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}' \
                        AND bahn_monitoring_prices.price > 100 \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {2} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0".format(self.track["start"], self.track["end"], self.offset)
        result = self.connection.select(query)
        if result is not None and result[0]["maximum"] is not None:
            maximum = result[0]["maximum"]
        return self.float(maximum)

    def minimum(self):
        minimum = 0.0
        query = "SELECT \
                        MIN(bahn_monitoring_prices.price) as minimum \
                        FROM bahn_monitoring_prices \
                        INNER JOIN bahn_monitoring_connections on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
                        WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}' \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {2} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0".format(self.track["start"], self.track["end"], self.offset)
        result = self.connection.select(query)
        if result is not None and result[0]["minimum"] is not None:
            minimum = result[0]["minimum"]
        return self.float(minimum)

    def getAggregatedData(self):
        data = {"days_with_prices": self.dailyaverage(), "minimum": self.minimum(), "maximum": self.maximum(), "average": self.average(), "datapoints": self.datapoints(), "maximumpricejump_up": self.maxjumpup(),  "maximumpricejump_down": self.maxjumpdown()}
        #Set redis cache for 6 hours
        self.redis.setex(self.getRedisPath(), datetime.timedelta(hours=6), value=json.dumps(data))

    def getRedisPath(self):
        return "trackprice_{0}_{1}".format(self.track["start"], self.track["end"])

class ConnectionPrices:
    def __init__(self, db, connection_id, redis):
        self.offset = 130
        self.db = db
        self.redis = redis
        self.connection_id = connection_id
        self.info = None

    def float(self, value):
        return round(float(value), 2)

    def int(self, value):
        return int(value)

    def datapoints(self):
        #Get count of datapoints collected for this connection
        query = "SELECT \
                        COUNT(bahn_monitoring_prices.id) as count \
                        FROM bahn_monitoring_prices \
                        WHERE bahn_monitoring_prices.connection_id = '{0}' \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {1} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0".format(self.connection_id, self.offset)
        result = self.db.select(query)
        if result is not None and result[0]["count"] is not None:
            return self.int(result[0]["count"])

    def average(self):
        #Get overall average for this connection
        query = "SELECT \
                        ROUND(avg(bahn_monitoring_prices.price), 2) as average_price, \
                        DATEDIFF(bahn_monitoring_connections.starttime, bahn_monitoring_prices.time) AS days_to_train_departure \
                        FROM bahn_monitoring_connections \
                        INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
                        WHERE bahn_monitoring_connections.id = '{0}' \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {1} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0".format(self.connection_id, self.offset)
        result = self.db.select(query)
        if result is not None and result[0]["average_price"] is not None:
            return self.float(result[0]["average_price"])

    def dailyaverage(self):
        #Get average prices grouped by days until the train departs (days_to_train_departure)
        query = "SELECT \
                        ROUND(avg(bahn_monitoring_prices.price), 2) as average_price, \
                        DATEDIFF(bahn_monitoring_connections.starttime, bahn_monitoring_prices.time) AS days_to_train_departure \
                        FROM bahn_monitoring_connections \
                        INNER JOIN bahn_monitoring_prices on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
                        WHERE bahn_monitoring_connections.id = '{0}' \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {1} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0 \
                        GROUP BY days_to_train_departure \
                        HAVING days_to_train_departure IN (1,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,69,70,71,79,80,81,89,90,91,99,100,101,109,110,111,119,120,121,129,130,131,139,140,141) \
                        ORDER BY bahn_monitoring_prices.time ASC".format(self.connection_id, self.offset)
        _days_with_prices = {}
        for row in self.db.select(query):
            _days_with_prices[row["days_to_train_departure"]] = row["average_price"]
        return _days_with_prices

    def maxjumpup(self):
        #Calculate highest price jump up
        max=0.0
        last=0.0
        for days_to_train_departure, price in self.dailyaverage().items():
            if last == 0.0:
                last = price
                max = price
                continue
            if price > last and price - last > max:
                max = price - last
        return self.float(max)

    def maxjumpdown(self):
        #Calculate highest price jump down
        max=0.0
        last=0.0
        for days_to_train_departure, price in self.dailyaverage().items():
            if last == 0.0:
                last = price
                max = price
                continue
            if price < last and last - price > max:
                max = last -price
        return self.float(max)

    def maximum(self):
        #Get highest price
        maximum = 0.0
        query = "SELECT \
                        MAX(DISTINCT bahn_monitoring_prices.price) as maximum \
                        FROM bahn_monitoring_prices \
                        WHERE bahn_monitoring_prices.connection_id = '{0}' \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {1} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0".format(self.connection_id, self.offset)
        result = self.db.select(query)
        if result is not None and result[0]["maximum"] is not None:
            maximum = result[0]["maximum"]

        #Hacky workarround, mysql MAX function does not return values over 99.0 when > 100 is not given. Wtf.
        #Query again for values > 100
        query = "SELECT \
                        MAX(DISTINCT bahn_monitoring_prices.price) as maximum \
                        FROM bahn_monitoring_prices \
                        WHERE bahn_monitoring_prices.connection_id = '{0}' \
                        AND bahn_monitoring_prices.price > 100 \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {1} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0".format(self.connection_id, self.offset)
        result = self.db.select(query)
        if result is not None and result[0]["maximum"] is not None:
            maximum = result[0]["maximum"]
        return self.float(maximum)

    def minimum(self):
        #Get lowest price
        #todo
        minimum = 0.0
        query = "SELECT \
                        MIN(bahn_monitoring_prices.price) as minimum \
                        FROM bahn_monitoring_prices \
                        WHERE bahn_monitoring_prices.connection_id = '{0}' \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) < {1} \
                        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0".format(self.connection_id, self.offset)
        result = self.db.select(query)
        if result is not None and result[0]["minimum"] is not None:
            minimum = result[0]["minimum"]
        return self.float(minimum)

    def getInfo(self):
        #some more caching, since this function is called multiple times
        if self.info is not None:
            return self.info
        query = "SELECT \
                        * \
                        FROM bahn_monitoring_connections \
                        WHERE bahn_monitoring_connections.id = '{0}'".format(self.connection_id)
        result = self.db.select(query)
        if result is not None and result[0] is not None:
            self.info = result[0]
            return result[0]

    def getAggregatedData(self):
        data =  {"start": self.getInfo()['start'], "end": self.getInfo()['end'], "starttime": self.getInfo()['starttime'].strftime("%Y-%m-%d %H:%M:%S"), "days_with_prices": self.dailyaverage(), "minimum": self.minimum(), "maximum": self.maximum(), "average": self.average(), "datapoints": self.datapoints(), "maximumpricejump_up": self.maxjumpup(),  "maximumpricejump_down": self.maxjumpdown()}
        #Set redis cache for 6 hours
        self.redis.setex(self.getRedisPath(), datetime.timedelta(hours=6), value=json.dumps(data))

    def getRedisPath(self):
        return "connection_{0}".format(self.connection_id)

class Statistics:
    def __init__(self, db):
        self.db = db
        offset = 130
        self.offset = offset.getoffset

    def prices_to_weekdays(self):
        query = "SELECT \
        ROUND(AVG(bahn_monitoring_prices.price), 2) as average, \
        WEEKDAY(bahn_monitoring_prices.time) AS weekday \
        FROM bahn_monitoring_prices \
        WHERE DATEDIFF(NOW(), bahn_monitoring_prices.time) < {0} \
        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0 \
        GROUP by weekday".format(self.offset)
        return self.db.select(query)

    def lowest_price_per_weekday(self):
        query = "SELECT \
        ROUND(AVG(bahn_monitoring_prices.price), 2) as average, \
        WEEKDAY(bahn_monitoring_prices.time) AS weekday \
        FROM bahn_monitoring_prices \
        WHERE DATEDIFF(NOW(), bahn_monitoring_prices.time) < {0} \
        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0 \
        GROUP by weekday \
        ORDER by average ASC \
        LIMIT 1".format(self.offset)
        return self.db.select(query)

    def highest_price_per_weekday(self):
        query = "SELECT \
        ROUND(AVG(bahn_monitoring_prices.price), 2) as average, \
        WEEKDAY(bahn_monitoring_prices.time) AS weekday \
        FROM bahn_monitoring_prices \
        WHERE DATEDIFF(NOW(), bahn_monitoring_prices.time) < {0} \
        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0 \
        GROUP by weekday \
        ORDER by average DESC \
        LIMIT 1".format(self.offset)
        return self.db.select(query)

    def global_average(self):
        query = "SELECT \
        ROUND(AVG(bahn_monitoring_prices.price), 2) as average \
        FROM bahn_monitoring_prices \
        WHERE DATEDIFF(NOW(), bahn_monitoring_prices.time) < {0} \
        AND DATEDIFF(NOW(), bahn_monitoring_prices.time) >= 0".format(self.offset)
        return self.db.select(query)

    def activeconnections(self):
        query = "SELECT COUNT(id) as counter FROM bahn_monitoring_connections WHERE active = 1"
        result = self.db.select(query)
        if result is not None and result[0]["counter"] is not None:
            return result[0]["counter"]

    def connections(self):
        query = "SELECT COUNT(id) as counter FROM bahn_monitoring_connections"
        result = self.db.select(query)
        if result is not None and result[0]["counter"] is not None:
            return result[0]["counter"]

    def stationcount(self):
        query = "SELECT COUNT(id) as counter FROM bahn_monitoring_stations"
        result = self.db.select(query)
        if result is not None and result[0]["counter"] is not None:
            return result[0]["counter"]

    def hourlyrequests(self):
        query = "SELECT COUNT(id) as counter FROM bahn_monitoring_prices WHERE bahn_monitoring_prices.time >= DATE_SUB(NOW(), INTERVAL 1 HOUR)"
        result = self.db.select(query)
        if result is not None and result[0]["counter"] is not None:
            return result[0]["counter"]

    def dailyrequests(self):
        query = "SELECT COUNT(id) as counter FROM bahn_monitoring_prices WHERE bahn_monitoring_prices.time >= DATE_SUB(NOW(), INTERVAL 1 DAY)"
        result = self.db.select(query)
        if result is not None and result[0]["counter"] is not None:
            return result[0]["counter"]