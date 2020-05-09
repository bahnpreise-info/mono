import _thread, time, os, redis
from includes import scheduler, connectionmanager, statistic_cacher, tracks_cacher, connections_cacher
from configparser import ConfigParser
from orator import DatabaseManager

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

#_thread.start_new_thread( scheduler.Scheduler, () )
#_thread.start_new_thread( connectionmanager.ConnectionManager, ())
_thread.start_new_thread( statistic_cacher.StatisticsCalculator, (db, r))
#_thread.start_new_thread( tracks_cacher.TracksCacher, (db, r,))
#_thread.start_new_thread( connections_cacher.ConnectionsCacher, (db, r,))

while True:
  time.sleep(10)
