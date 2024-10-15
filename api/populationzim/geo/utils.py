

def wkt2Array(string):
    multiPoly = string.lstrip('MULTIPOLYGON').lstrip("(((").rstrip(")))").split("),(")
    polyArray = []
    for poly in multiPoly: polyArray.append([[[float(latlon.split(" ")[1]), float(latlon.split(" ")[0])] for latlon in poly.split(",")]])
    return polyArray
