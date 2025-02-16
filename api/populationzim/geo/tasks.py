from celery import Celery
import os


app = Celery("tasks",broker="pyamqp://tendaiwbm:tendai2systems@172.17.0.4:5672/popzim")

@app.task
def add(x,y):
    return(x + y)


