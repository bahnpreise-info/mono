import _thread, time, os
from includes import scheduler, connectionmanager, statistic_cacher

os.chdir("/opt/app")

_thread.start_new_thread( scheduler.Scheduler, () )
_thread.start_new_thread( connectionmanager.ConnectionManager, () )
_thread.start_new_thread( statistic_cacher.StatisticsCalculator, () )

while True:
  time.sleep(10)
