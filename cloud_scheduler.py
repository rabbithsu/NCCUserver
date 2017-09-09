import os
import sys
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig()

def my_job():
	print "Start: "+time.strftime("%Y%m%d")
	os.system("sh cloud.sh")
 
sched = BlockingScheduler()
sched.add_job(my_job, 'interval', days = 1)
sched.start()

