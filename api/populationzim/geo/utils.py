from geo.worker import request_handler
from django.http import JsonResponse
import math

def extract_ring(polygon):
    return [[float(point.split(" ")[1]),float(point.split(" ")[0])] for point in polygon.split(",")]

def reconstruct_multi(polygons):
    multi = []
    outerRing = extract_ring(polygons[0])
    multi.append(outerRing)
    if len(polygons) > 1:
        for polygon in polygons[1:]:
            innerRing = list(reversed(extract_ring(polygon)))
            #innerRing += [[0,0] for i in range(len(outerRing)-len(innerRing))]
            multi.append(innerRing) 
    return multi

def prepare_distribution(decoratee):
    def wrapper(query):
        queryResult = decoratee(query)
        geom = (pair[1] for pair in queryResult)
        shapes = []
        for mPoly in geom:
            mp = mPoly.replace("MULTIPOLYGON","").strip("(((").strip(")))").split("), (")
            if len(mp) == 1:
                polygons = mp[0].split("),(")
                multiPoly = [reconstruct_multi(polygons)]
            elif len(mp) > 1:
                multiPoly = []
                for poly in mp:
                    polygons = poly.split("),(")
                    multiPoly.append([reconstruct_multi(polygons)])
            shapes.append(multiPoly)
        RESPONSE = {
                    "coordinates": shapes,
                    "admin-level": "district",
                    "grain": "ward",
                    "values": [math.log10(pair[0]) if pair[0] > 0 else pair[0] for pair in queryResult],
                   }
        return JsonResponse(RESPONSE)
    return wrapper

def prepare_admin_names(decoratee):
    def wrapper(query):
        return JsonResponse({query.GET["admin"]:[admin[0] for admin in decoratee(query)]})
    return wrapper

@request_handler
def query_munyayi(query):
    return query

