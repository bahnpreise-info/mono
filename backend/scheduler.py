from includes import mysql
import datetime, os, schiene, random, configparser, logging, time, pytz
from orator import DatabaseManager
from multiprocessing import Pool, Lock
os.chdir("/opt/app") #change this according to your needs - working directory

class Scheduler():

    def __init__(self):
        self.status = {}    #saves the status (true/false) of important jobs
        self.status['logger'] = self.setupLogger()
        self.local = pytz.timezone("Europe/Berlin")

        if self.status['logger']:
            self.status['database'] = self.setupDatabase()
        else:
            print("FATAL ERROR: Could not setup a logger. Stopped execution.")
            self.status['database'] = False

        if self.status['logger'] == True and self.status['database'] == True:
            self.checkConnections()


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

    def setupDatabase(self):
        try:
            config = configparser.ConfigParser()
            config.readfp(open('connectionmanager.ini'))
            host = config.get('database', 'host')
            database = config.get('database', 'database')
            user = config.get('database', 'user')
            password = config.get('database', 'password')
            self.databasePrefix = config.get('database', 'database_prefix')
        except Exception as e:
            self.logger.error("Could not fetch connectionmanager.ini: %s", e)
            return False

        self.conDatabase = mysql.Database(host, database, user, password, self.logger)

        if self.conDatabase.connect():
            try:
                self.conDatabase.createTable(self.databasePrefix+"connections", ['start VARCHAR(100)', 'end VARCHAR(100)', 'starttime TIMESTAMP', 'endtime TIMESTAMP', 'next_scrape TIMESTAMP', 'active INT'])
                self.conDatabase.createTable(self.databasePrefix+"stations", ['name VARCHAR(100)', 'stationid VARCHAR(30)'])
                self.conDatabase.createTable(self.databasePrefix+"prices", ['price VARCHAR(10)', 'connection_id INT'])
                self.conDatabase.close()
            except Exception as e:
                self.logger.error("Could not create Tables: %s", e)
                return False
            self.logger.debug("Succesfuly connected to database.")
            return True
        else:
            self.logger.error("Could not connect to to Database.")
            return False

    def checkConnections(self):
        self.conDatabase.connect()
        connections = self.conDatabase.selectFrom(self.databasePrefix+"connections", 'id, start, end, starttime, endtime', 'active = 1 AND next_scrape < "'+datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")+'"')
        self.conDatabase.close()

        self.logger.debug("Connections to process: {}".format(connections))

        if connections != False:
            for connection in connections:
                self.logger.debug("Processing connection with id {}".format(connection['id']))
                self.updateConnection(connection)
        else:
            self.logger.error("Not able to select connections.")
            return False

    def updateConnection(self, c):
        connection = self.getConnection(c["start"], c["end"], c["starttime"])
        if connection != False:
            if self.getStarttime(c["starttime"], connection['departure']) == c["starttime"] and self.getEndtime(c["starttime"], connection['duration']) == c["endtime"]:
                timedelta = (c["starttime"]-datetime.datetime.now())/datetime.timedelta(hours=1)
                self.conDatabase.connect()

                if connection['price'] == None:
                    connection['price'] = 0

                if timedelta > 30:  #if more then 30 hours: next scrape in 10-26 hours
                    randomDate = datetime.datetime.utcnow()+datetime.timedelta(hours=random.randint(10, 25), minutes=random.randint(0,59))
                    self.conDatabase.update([['next_scrape', '"'+randomDate.strftime('%Y-%m-%d %H:%M:%S')+'"']], self.databasePrefix+"connections", "id = "+str(c["id"]))
                elif timedelta > 10:  #if 10-30 hours: next scrape in 8-10 hours
                    randomDate = datetime.datetime.utcnow()+datetime.timedelta(hours=random.randint(8, 9), minutes=random.randint(0,59))
                    self.conDatabase.update([['next_scrape', '"'+randomDate.strftime('%Y-%m-%d %H:%M:%S')+'"']], self.databasePrefix+"connections", "id = "+str(c["id"]))
                elif timedelta > 5:  #if 5-10 hours: next scrape in 2 hours
                    randomDate = datetime.datetime.utcnow()+datetime.timedelta(hours=2)
                    self.conDatabase.update([['next_scrape', '"'+randomDate.strftime('%Y-%m-%d %H:%M:%S')+'"']], self.databasePrefix+"connections", "id = "+str(c["id"]))
                elif timedelta < 1:  #if less then 1 hours: set connection to inactive
                    self.conDatabase.update([['active', 0]], self.databasePrefix+"connections", "id = "+str(c["id"]))

                if self.conDatabase.insertInto(self.databasePrefix+"prices", [['price', connection['price']], ['connection_id', c["id"]]]):
                    returnval = True
                else:
                    self.logger.error("Not able to insert price")
                    returnval = False

                self.conDatabase.close()
                return returnval
        else:
            self.logger.error("Not able to get Connection.")
            self.deleteconnection(c["id"])
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
            ret["price"] = connections[0]['price']
        except:
            self.logger.error("Not able to create Connection")
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

    def deleteconnection(self, id):
        self.logger.debug("Deleting connection with ID {}".format(id))
        try:
            config = configparser.ConfigParser()
            config.readfp(open('connectionmanager.ini'))
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
            db.table('bahn_monitoring_connections').where('id', '=', id).delete()
            db.table('bahn_monitoring_prices').where('connection_id', '=', id).delete()
        except:
            return False

while True:
  Scheduler()
  time.sleep(10)
