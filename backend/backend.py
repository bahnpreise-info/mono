import _thread, time, os
from includes import scheduler, connectionmanager, statisticscalculator

os.chdir("/opt/app")

_thread.start_new_thread( scheduler.Scheduler, () )
_thread.start_new_thread( connectionmanager.ConnectionManager, () )
_thread.start_new_thread( statisticscalculator.StatisticsCalculator, () )

while True:
  time.sleep(10)
