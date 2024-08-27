# -*- encoding: utf-8 -*-
# @ModuleName: auto_restart
# @Function :
# @Author : ximo
# @Time : 2022/11/22 15:28
# BlockingScheduler定时任务
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os
import subprocess


def start():
    x = os.system("bash ./auto_run.sh")
    print(x)
    # proc = subprocess.Popen("ls -l", shell=True, stdout=subprocess.PIPE)
    # stdout_value, stderr_value = proc.communicate(' ')
    # print(stdout_value, stderr_value)


def stop():
    x = os.system("bash ./auto_stop.sh")
    print(x)


# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(func=start, trigger='cron', hour='3', minute="25")
scheduler.add_job(func=stop, trigger='cron', hour='3', minute="20")
scheduler.start()
