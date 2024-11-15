import os,sys
sys.path.insert(0,'./vabatsiri')
from vabatsiri.db import QExecutor as dbg
import psycopg2
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())


def tumira(query):
    connection = psycopg2.connect(user=os.getenv('PG_USER'),
                                  password=os.getenv('PG_PASSWORD'),
                                  host=os.getenv('HOST'),
                                  port=os.getenv('PORT'),
                                  database=os.getenv('DATABASE'),
                                  options=os.getenv('OPTIONS'))
    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()

def extract_ring(polygon):
    return [[float(point.split(" ")[1]),float(point.split(" ")[0])] for point in polygon.split(",")]

def reconstruct_multi(polygons):
    multi = []
    outerRing = extract_ring(polygons[0])
    multi.append(outerRing)
    if len(polygons) > 1:
        for polygon in polygons[1:]:
            innerRing = list(reversed(extract_ring(polygon)))
            innerRing += [[0,0] for i in range(len(outerRing)-len(innerRing))]
            multi.append(innerRing) 
    return multi

def wkt2Array():
    for admin in ["ward","district","province"]:
        print(f"converting WKT to ARRAY for table {admin}")
        query = "SELECT ST_ASTEXT(shape),"
        if admin == "ward": query = " ".join([query,"ward_number, district_name"])
        else:               query = " ".join([query,f"{admin}_name"])
        query = " ".join([query,f"FROM prelim.{admin}"])
        queryResult = tumira(query)
        geom = [row[0] for row in queryResult]
        if admin == "ward":
            ward = [row[1] for row in queryResult]
            district = [row[2] for row in queryResult]
        else:
            admin_names = [row[1] for row in queryResult]
        QUERY = """"""
        for idx,mPoly in enumerate(geom): 
            mPoly = mPoly.replace("MULTIPOLYGON","").strip("(((").strip(")))").split("), (")
            if len(mPoly) == 1:
                polygons = mPoly[0].split("),(")
                multiPoly = [reconstruct_multi(polygons)]
            elif len(mPoly) > 1:
                multiPoly = []
                for poly in mPoly:
                    polygons = poly.split("),(")
                    multiPoly.append([reconstruct_multi(polygons)])
            if admin == "ward":
                QUERY += f"""UPDATE prelim.ward
                             SET geom = ARRAY{multiPoly}
                             WHERE ward_number = {ward[idx]}
                             AND district_name = '{district[idx]}';"""
            else:
                QUERY += f"""UPDATE prelim.{admin}
                             SET geom = ARRAY{multiPoly}
                             WHERE {admin}_name = '{admin_names[idx]}';"""
            
        dbg.exec(QUERY)

if __name__ == "__main__":
    wkt2Array()
