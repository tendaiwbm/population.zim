from django.http import JsonResponse
from geo.data_validation import distro_validator,admin_validator
from geo.utils import query_munyayi,prepare_distribution,prepare_admin_names

@prepare_distribution
def fetch_distribution(request):
    if distro_validator(request.GET):
        query = f"""select {request.GET['sex']}_population_density_{request.GET['year']},geom from prelim.ward """
        if "admin-names" in request.GET:
            query = " ".join([query,f"""where {request.GET['admin']}_name in""","""""".join(["(",",".join([f"'{name}'" for name in request.GET["admin-names"].split(";")]),")"])])
        return query_munyayi(query)

@prepare_admin_names
def fetch_admin_names(request):
    if admin_validator(request.GET):
        query = f"""SELECT {request.GET['admin']}_name FROM prelim.{request.GET['admin']}"""
        return query_munyayi(query)
