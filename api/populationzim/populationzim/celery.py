import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE","populationzim.settings")

app = Celery("populationzim")

app.config_from_object("django.conf:settings",namespace="CELERY")

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print("Hosanna in the highest")
