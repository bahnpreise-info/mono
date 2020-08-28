import _thread, time, os, redis
from includes import scheduler, connectionmanager, statistic_cacher
from includes.functions import Logger, ConnectionPrices, TrackPrices, Offset
from configparser import ConfigParser
from orator import DatabaseManager
from multiprocessing import Pool

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

#Logger instance
logger = Logger("Backend")

#Orator instance
db = DatabaseManager(oratorconfig)

#Redis instance
r = redis.Redis(host=config.get('redis', 'host'), password=config.get('redis', 'password'))

#These can run single threaded
_thread.start_new_thread( scheduler.Scheduler, () )
_thread.start_new_thread( connectionmanager.ConnectionManager, ())
_thread.start_new_thread( statistic_cacher.StatisticsCalculator, (db, r))

#connection cache function
def connection_cache(connection):
  logger.write("Processing {0} -> {1} @ {2}".format(connection["start"], connection["end"], connection["starttime"]))
  connectiondb = ConnectionPrices(db, connection["id"], r)
  connectiondb.getAggregatedData() #we don't need the result, but the function refreshed the cache

#track cache function
def track_cache(track):
  logger.write("Processing {0} -> {1}".format(track["start"], track["end"]))
  trackdb = TrackPrices(db, track, r)
  trackdb.getAggregatedData() #we don't need the result, but the function refreshed the cache

while True:
  #Pool worker
  pool = Pool(4)
  #cache connections
  for connection in db.table('bahn_monitoring_connections').where('active', '1').get():
    pool.apply_async(connection_cache, (connection,))

  #cache tracks
  for track in db.table('bahn_monitoring_connections').where('active', '1').distinct().get():
    pool.apply_async(track_cache, (track,))
  pool.close()
  pool.join()