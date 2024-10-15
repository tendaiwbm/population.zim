from django.http import JsonResponse
from . import worker


def fetch_distribution(request):
    return JsonResponse(worker.request_handler(request.GET))

def toraZvakavanda(request):
    return JsonResponse({"version":1})
