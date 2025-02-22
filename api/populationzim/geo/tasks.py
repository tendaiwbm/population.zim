from celery import shared_task,chord
import os


#app = Celery("tasks",broker="pyamqp://tendaiwbm:tendai2systems@172.17.0.4:5672/popzim")

#app.task
def add(x,y):
    return(x + y)

@shared_task
def format_polygon(polygon):
    if len(polygon[0]) == 1:
        return polygon
    else:
        return [[polygon[0][0],[point for point in polygon[0][1] if point != [0,0]]]]

@shared_task
def combine_polygons(polygons):
    return polygons

def geom_entrypoint(polygons):
    return chord(format_polygon.s(polygon) for polygon in polygons)(combine_polygons.s())




