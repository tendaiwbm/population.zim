import sys
sys.path.insert(0,'./vabatsiri')
from vabatsiri.db import QExecutor as dbg
import psycopg2


def extractRing(polygon):
    return [[float(point.split(" ")[1]),float(point.split(" ")[0])] for point in polygon.split(",")]

def wkt2Array():
    for admin in ["ward"]:
        queryResult = tumira(f"""SELECT ward_number,district_name,ST_ASTEXT(shape) FROM prelim.{admin}""")
        geom = [row[2] for row in queryResult]
        ward = [row[0] for row in queryResult]
        district = [row[1] for row in queryResult]
        QUERY = """"""
        for idx,mPoly in enumerate(geom): 
            mPoly = mPoly.replace("MULTIPOLYGON","").strip("(((").strip(")))").split("), (")
            if len(mPoly) == 1:
                polygons = mPoly[0].split("),(")
                if len(polygons) == 1:
                    multiPoly = [[extractRing(polygons[0])]]
                elif len(polygons) == 2:
                    innerRing = extractRing(polygons[1])
                    outerRing = list(reversed(extractRing(polygons[0])))
                    innerRing += [[0,0] for i in range(len(outerRing)-len(innerRing))]
                    multiPoly = [[outerRing,innerRing]]
            elif len(mPoly) > 1:
                multiPoly = []
                for poly in mPoly:
                    polygons = poly.split("),(")
                    if len(polygons) == 1:
                        multiPoly.append([extractRing(polygons[0])])
                    elif len(polygons) == 2:
                        innerRing = extractRing(polygons[1])
                        outerRing = extractRing(polygons[0])
                        multiPoly.append([outerRing,innerRing])

            QUERY += f"""UPDATE prelim.ward
                         SET geom = ARRAY{multiPoly}
                         WHERE ward_number = {ward[idx]}
                         AND district_name = '{district[idx]}';"""
        dbg.exec(QUERY)

if __name__ == "__main__":
    wkt2Array()
