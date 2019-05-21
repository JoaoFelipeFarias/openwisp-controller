import hashlib
from django.utils import timezone
from datetime import timedelta
import django

django.setup()
from background_task.models import Task

cheap_hash = lambda input: hashlib.md5(input).hexdigest()[:6]



class BackgroundTaskCreator():
    global cheap_hash
    def create_tasks():
        task_names = ['portal.tasks.coovadevicepool',

                      ]

        run_at = [timezone.now()]
                  # timezone.now(),
                  # timezone.now().replace(hour=8,minute=0, second=0)]

        repeat = [10]
                  # 60,
                  # 60 * 60 * 24]

        Task.objects.all().delete()
        for task_number in range(len(task_names)):
            encoded_str = task_names[task_number].encode('utf-8')
            hash = cheap_hash(encoded_str)
            Task.objects.create(
                task_name=task_names[task_number],
                task_params="[[], {}]",
                task_hash=hash,
                priority=0,
                run_at= run_at[task_number],
                repeat=repeat[task_number],

            )

        print(Task.objects.all().values('task_name'))
        return
