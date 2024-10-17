from django.http import JsonResponse
from geo.data_validation import distro_validator
from geo.utils import queryMunyayi,wkt2Array

@wkt2Array
def fetch_distribution(request):
    if distro_validator(request.GET):
        query = f"""select {request.GET['sex']}_population_{request.GET['year']},st_astext(shape) from prelim.ward where district_name = 'Bulawayo'"""
        return queryMunyayi(query)

def toraZvakavanda(request):
    return JsonResponse({"version":1})
