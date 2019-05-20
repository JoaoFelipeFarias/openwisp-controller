import os
import sys
import subprocess
import traceback
import datetime
import time

def process_tasks():
    create_task = True
    while True:
        try:
            if create_task:
                create_task = False
                task = subprocess.Popen('python3 manage.py process_tasks', shell=True)
                print(str(datetime.datetime.now()) + ' created manage.py process tasks\n')

            time.sleep(30)
            process_status = task.poll()
            if process_status is not None:
                print(str(datetime.datetime.now()) + ' manage.py process tasks closed with a error, will attempt to restart\n')
                create_task = True

        except subprocess.CalledProcessError as e:
            with open('error.txt', 'a') as testfile:
                testfile.write(str(datetime.datetime.now()) + str(traceback.print_exc()) + '\n')
            task.terminate()
            print(str(datetime.datetime.now()) + ' manage.py process tasks entered in exception subprocess, will attempt to restart\n')
            create_task = True