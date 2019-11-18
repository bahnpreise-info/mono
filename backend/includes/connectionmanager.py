from includes import mysql
import configparser, os, logging, schiene, random, datetime, time, pytz

class ConnectionManager():
    def __init__(self):
        self.maxActiveConnections = 4000
        self.status = {}    #saves the status (true/false) of important jobs
        self.status['logger'] = self.setupLogger()

        if self.status['logger']:
            self.status['database'] = self.setupDatabase()
        else:
            print("FATAL ERROR: Could not setup a logger. Stopped execution.")
            self.status['database'] = False

        if self.status['logger'] == True and self.status['database'] == True:
            self.setConnections()

    def setupLogger(self):
        try:
            self.logger = logging.getLogger('Connectionmanager')
            self.logger.setLevel(logging.DEBUG)
            self.ch = logging.StreamHandler()
            self.ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.ch.setFormatter(formatter)
            self.logger.addHandler(self.ch)
            self.logger.debug("--------------------------------- START --------------------------------")
            self.logger.debug("Successfuly setup the logger.")
            self.local = pytz.timezone("Europe/Berlin")
            return True
        except:
            return False

    def setupDatabase(self):
        try:
            config = configparser.ConfigParser()
            config.readfp(open('database.ini'))
            host = config.get('database', 'host')
            database = config.get('database', 'database')
            user = config.get('database', 'user')
            password = config.get('database', 'password')
            self.databasePrefix = config.get('database', 'database_prefix')
        except Exception as e:
            self.logger.error("Could not fetch database.ini: %s", e)
            return False

        self.conDatabase = mysql.Database(host, database, user, password, self.logger)

        if self.conDatabase.connect():
            try:
                self.conDatabase.createTable(self.databasePrefix+"connections", ['start VARCHAR(100)', 'end VARCHAR(100)', 'starttime TIMESTAMP', 'endtime TIMESTAMP', 'next_scrape TIMESTAMP', 'active INT'])
                self.conDatabase.createTable(self.databasePrefix+"stations", ['name VARCHAR(100)', 'stationid VARCHAR(30)'])
                self.conDatabase.close()
            except Exception as e:
                self.logger.error("Could not create Tables: %s", e)
                return False
            self.logger.debug("Succesfuly connected to database.")
            return True
        else:
            self.logger.error("Could not connec to to Database.")
            return False

    def setConnections(self):
        self.conDatabase.connect()
        connections = self.conDatabase.selectFrom(self.databasePrefix+"connections", 'COUNT(*)', 'active = 1')
        self.conDatabase.close()

        if connections != False:
            print (connections[0]['COUNT(*)'])
            if connections[0]['COUNT(*)'] >= self.maxActiveConnections:
                self.logger.debug("Maximum of Connections already active")
                return True
            else:
                i = connections[0]["COUNT(*)"]
                while i <= self.maxActiveConnections:
                    res = self.createConnection()
                    if res == False:
                        self.logger.error("Not able to create Connection.")
                    else:
                        i += 1

        else:
            self.logger.error("Not able to select data from the Database.")
            return False

    def createConnection(self):
        stations_list = []
        self.conDatabase.connect()
        stations = self.conDatabase.selectFrom(self.databasePrefix+"stations", 'name', 'id > 0')
        self.conDatabase.close()

        if stations != False and len(stations) > 1:
            for station in stations:
                stations_list.append(station['name'])
        else:
            self.logger.error("Not able to select stations or stations empty.")
            return False

        stationStart = random.choice(stations_list)
        stationEnd = stationStart

        while stationEnd == stationStart:
            stationEnd = random.choice(stations_list)

        days = random.randint(90, 170)
        hours = random.randint(0,23)
        minutes = random.randint(0,59)

        timeStart = datetime.datetime.now() + datetime.timedelta(days=days , hours=hours , minutes=minutes)

        connection = self.getConnection(stationStart, stationEnd, timeStart)

        if connection != False:
            startTime = self.getStarttime(timeStart, connection['departure'])
            endTime = self.getEndtime(startTime, connection["duration"])

            if endTime != False and startTime != False:
                self.conDatabase.connect()
                if self.conDatabase.insertInto(self.databasePrefix+"connections", [['start', connection['stationStart']], ['end', connection['stationEnd']], ['starttime', startTime.strftime('%Y-%m-%d %H:%M:%S')], ['endtime', endTime.strftime('%Y-%m-%d %H:%M:%S')], ['next_scrape', datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')], ['active', 1]]):
                    return True
                else:
                    self.logger.error("Not able to insert Connection")
                    return False
                self.conDatabase.close()
            else:
                self.logger.error("Not able to calc start and end time")
                return False
        else:
            self.logger.error("Not able to create Connection")
            return False


    def getConnection(self, stationStart, stationEnd, timeStart):
        ret = {}
        conSchiene = schiene.Schiene()

        try:
            connections = conSchiene.connections(stationStart, stationEnd, dt=timeStart)
            ret["stationStart"] = stationStart
            ret["stationEnd"] = stationEnd
            ret["products"] = connections[0]['products']
            ret["departure"] = connections[0]['departure']
            ret["duration"] = connections[0]['time']
            ret["departure"] = connections[0]['departure']
        except Exception as e:
            self.logger.error("Not able to create Connection for %s - %s at %s: %s", stationStart, stationEnd, timeStart, e)
            return False

        return ret

    def getStarttime(self, timeStart, departure):
        hour1 = timeStart.strftime("%H")
        min1 = timeStart.strftime("%M")

        hour2 = departure[0:2]
        min2 = departure[3:5]

        if hour2 < hour1:
            timeStart += datetime.timedelta(days=1)
            return datetime.datetime.strptime(timeStart.strftime("%Y-%m-%d ")+departure, "%Y-%m-%d %H:%M")
        elif hour2 == hour1 and min2 < min1:
            timeStart += datetime.timedelta(days=1)
            return datetime.datetime.strptime(timeStart.strftime("%Y-%m-%d ")+departure, "%Y-%m-%d %H:%M")
        else:
            return datetime.datetime.strptime(timeStart.strftime("%Y-%m-%d ")+departure, "%Y-%m-%d %H:%M")

    def getEndtime(self, starttime, duration):
        dur = duration.split(':')
        try:
            return starttime+datetime.timedelta(hours=int(dur[0]), minutes=int(dur[1]))
        except:
            return False
