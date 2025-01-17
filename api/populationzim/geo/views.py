from geo.data_validation import distro_validator,admin_validator
from geo.utils import query_munyayi,prepare_distribution,prepare_admin_names

@prepare_distribution
def fetch_distribution(request):
    if distro_validator(request.GET):
        
        if request.GET['grain'] == "ward":
            query = f"""select {request.GET['sex']}_population_density_{request.GET['year']},geom from prelim.{request.GET['grain']}"""
            if "admin-names" in request.GET:
                query = " ".join([query,f"""where {request.GET['admin']}_name in""","""""".join(["(",",".join([f"'{name}'" for name in request.GET["admin-names"].split(";")]),")"])])
        
        elif request.GET['grain'] in ["district","province"]:
            query = f"""
                        SELECT sum(b.{request.GET['sex']}_population_density_{request.GET['year']}),geom
                        FROM prelim.{request.GET['grain']} AS a
                        JOIN 
                     """
            subQuery = f"""(SELECT {request.GET['sex']}_population_density_{request.GET['year']},{request.GET['admin']}_name
                           FROM prelim.ward""" 
            if "admin-names" in request.GET:
                subQuery = " ".join([subQuery,f"""WHERE {request.GET['admin']}_name in""","""""".join(["(",",".join([f"'{name}'" for name in request.GET["admin-names"].split(";")]),")"])])
            
            query = """""".join([query,subQuery, f""") as b ON a.{request.GET['admin']}_name = b.{request.GET['admin']}_name GROUP BY a.geom"""])
        return query_munyayi(query)

@prepare_admin_names
def fetch_admin_names(request):
    if admin_validator(request.GET):
        query = f"""SELECT {request.GET['admin']}_name FROM prelim.{request.GET['admin']}"""
        return query_munyayi(query)
