from geo.worker import request_handler
from django.http import JsonResponse

def wkt2Array(decoratee):
    def wrapper(query):
        queryResult = decoratee(query)
        geom = [pair[1] for pair in queryResult]
        multiPoly = [string.lstrip('MULTIPOLYGON').lstrip("(((").rstrip(")))").split("),(") for string in geom]
        polyArray = []
        for mPoly in multiPoly: polyArray.append([[[float(latlon.split(" ")[1]), float(latlon.split(" ")[0])] for poly in mPoly for latlon in poly.split(",")]])
        RESPONSE = {
                    "coordinates": polyArray,
                    "admin-level": "district",
                    "select-one": False,
                    "grain": "ward",
                    "values": [pair[0] for pair in queryResult],
                   }
        return JsonResponse(RESPONSE)
    return wrapper

@request_handler
def queryMunyayi(query):
    return query

