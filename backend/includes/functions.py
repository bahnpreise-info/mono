import time

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
    def __init__(self, connection, track):
        self.connection = connection
        self.track = track

    def float(self, value):
        return round(float(value), 2)

    def int(self, value):
        return int(value)

    def datapoints(self):
        #Get overall average for this track
        query = "SELECT \
                        COUNT(bahn_monitoring_prices.id) as count \
                        FROM bahn_monitoring_prices \
                        INNER JOIN bahn_monitoring_connections on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
                        WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}'".format(self.track["start"], self.track["end"])
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
                        WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}'".format(self.track["start"], self.track["end"])
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
                        GROUP BY days_to_train_departure \
                        ORDER BY bahn_monitoring_prices.time ASC".format(self.track["start"], self.track["end"])
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
                        WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}'".format(self.track["start"], self.track["end"])
        result = self.connection.select(query)
        if result is not None and result[0]["maximum"] is not None:
            maximum = result[0]["maximum"]

        #Hacky workarround, mysql MAX function does not return values over 99.0 when > 100 is not given. Wtf.
        #Query again for values > 100
        query = "SELECT \
                        MAX(DISTINCT bahn_monitoring_prices.price) as maximum \
                        FROM bahn_monitoring_prices \
                        INNER JOIN bahn_monitoring_connections on (bahn_monitoring_connections.id = bahn_monitoring_prices.connection_id) \
                        WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}'  AND bahn_monitoring_prices.price > 100".format(self.track["start"], self.track["end"])
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
                        WHERE bahn_monitoring_connections.start = '{0}' AND bahn_monitoring_connections.end = '{1}'".format(self.track["start"], self.track["end"])
        result = self.connection.select(query)
        if result is not None and result[0]["minimum"] is not None:
            minimum = result[0]["minimum"]
        return self.float(minimum)