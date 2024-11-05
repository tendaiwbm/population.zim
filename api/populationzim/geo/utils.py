from geo.worker import request_handler
from django.http import JsonResponse
import math

def wkt2Array(decoratee):
    def wrapper(query):
        queryResult = decoratee(query)
        geom = [pair[1] for pair in queryResult]
        multiPoly = [string.lstrip('MULTIPOLYGON').lstrip("(((").rstrip(")))").split("),(") for string in geom]
        polyArray = []
        for mPoly in multiPoly: 
            polyList = []
            for poly in mPoly:
                polyCoordList = []
                for latlon in poly.split(","):
                    polyCoordList.append([float(latlon.split(" ")[1]), float(latlon.split(" ")[0])])
                polyList.append([polyCoordList])
            polyArray.append(polyList)
        RESPONSE = {
                    "coordinates": polyArray,
                    "admin-level": "district",
                    "grain": "ward",
                    "values": [math.log10(pair[0]) if pair[0] > 0 else pair[0] for pair in queryResult],
                   }
        return JsonResponse(RESPONSE)
    return wrapper

def prepareAdminNames(decoratee):
    def wrapper(query):
        return JsonResponse({query.GET["admin"]:[admin[0] for admin in decoratee(query)]})
    return wrapper

@request_handler
def queryMunyayi(query):
    return query

