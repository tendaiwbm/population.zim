import os,sys
from vabatsiri import db
from qgis.core import *
QgsApplication.setPrefixPath('/usr',True)
sys.path.insert(0,'./vabtsiri')
from qgis.core import QgsVectorLayer,QgsExpression,QgsFeatureRequest
from vabatsiri.db import QExecutor as dbg


def resolveMvurwi(layer):
    exp = ''' "ADM2_EN"  =  'Mazowe' or  "ADM2_EN"  =  'Mvurwi' '''
    layer.selectByExpression(exp)
    Mvurwi = [ward for ward in tuple(layer.getSelectedFeatures()) if ward.attributes()[2] == 'Mvurwi'][0]
    query = ''' '''
    
    d = {
                'district_name': Mvurwi.attributes()[2],
                'province_name': Mvurwi.attributes()[7],
                'shape': Mvurwi.geometry().asWkt(),
            }
    
    query += f'''UPDATE prelim.ward
                 SET shape = '{d['shape']}'
                 WHERE district_name = 'Mazowe'
                 AND ward_number = 28;\n'''
    
    query += '''UPDATE prelim.ward
                SET male_population_2022 = (SELECT SUM(male_population_2022) FROM prelim.ward WHERE district_name = 'Mvurwi'),
                    female_population_2022 = (SELECT SUM(female_population_2022) FROM prelim.ward WHERE district_name = 'Mvurwi'),
                    total_population_2022 = (SELECT SUM(total_population_2022) FROM prelim.ward WHERE district_name = 'Mvurwi'),
                    male_population_2012 = (SELECT SUM(male_population_2012) FROM prelim.ward WHERE district_name = 'Mvurwi'),
                    female_population_2012 = (SELECT SUM(female_population_2012) FROM prelim.ward WHERE district_name = 'Mvurwi'),
                    total_population_2012 = (SELECT SUM(total_population_2012) FROM prelim.ward WHERE district_name = 'Mvurwi'),
                    total_households_2022 = (SELECT SUM(total_households_2022) FROM prelim.ward WHERE district_name = 'Mvurwi'),
                    avg_householdsize_2022 = (SELECT (SUM(total_population_2022)/SUM(total_households_2022)::NUMERIC) FROM prelim.ward WHERE district_name = 'Mvurwi'),
                    total_households_2012 = (SELECT SUM(total_households_2012) FROM prelim.ward WHERE district_name = 'Mvurwi'),
                    avg_householdsize_2012 = (SELECT (SUM(total_population_2012)/SUM(total_households_2012)::NUMERIC) FROM prelim.ward WHERE district_name = 'Mvurwi')
                WHERE district_name = 'Mazowe' AND ward_number = 28;'''

    query += '''DELETE FROM prelim.ward
                WHERE district_name = 'Mvurwi';'''

    dbg.exec(query)


if __name__ == "__main__":
    resolveMvurwi(QgsVectorLayer(sys.argv[1]))


