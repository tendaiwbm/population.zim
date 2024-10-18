from django.http import JsonResponse
from geo.data_validation import distro_validator,admin_validator
from geo.utils import queryMunyayi,wkt2Array,prepareAdminNames

@wkt2Array
def fetch_distribution(request):
    if distro_validator(request.GET):
        query = f"""select {request.GET['sex']}_population_{request.GET['year']},st_astext(shape) from prelim.ward where district_name = 'Gokwe North'"""
        return queryMunyayi(query)

@prepareAdminNames
def fetch_admin_names(request):
    if admin_validator(request.GET):
        query = f"""SELECT {request.GET['admin']}_name FROM prelim.{request.GET['admin']}"""
        return queryMunyayi(query)
