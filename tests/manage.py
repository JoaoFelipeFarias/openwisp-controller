#!/usr/bin/env python
import os
import sys
from threading import Thread
import BackgroundThread

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'openwisp2.settings')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    #threading for coova pool tasks
    thread = Thread(target=BackgroundThread.process_tasks, args=[])
    thread.setDaemon(True)
    thread.start()

    from portal.seed_background_tasks import BackgroundTaskCreator

    BackgroundTaskCreator.create_tasks()


