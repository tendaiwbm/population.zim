from geo.worker import request_handler
from django.http import JsonResponse
import math

def prepare_distribution(decoratee):
    def wrapper(query):
        queryResult = decoratee(query)
        geom = (pair[1] for pair in queryResult)
        RESPONSE = {
                    "coordinates": [polygon if len(polygon[0]) == 1 else [[polygon[0][0],[point for point in polygon[0][1] if point != [0,0]]]] for polygon in geom],
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

