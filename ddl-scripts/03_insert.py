import os,sys
from vabatsiri import db
from qgis.core import *
QgsApplication.setPrefixPath('/usr',True)
sys.path.insert(0,'./vabtsiri')
from qgis.core import QgsVectorLayer
from vabatsiri.db import QExecutor as dbg



def insertProvince(layer):
    layer.selectAll()
    for province in layer.getSelectedFeatures():
        prov = province.attributes()[2]
        if prov.startswith('Mat'): prov = prov[0:3] + 'e' + prov[4:]
        query = f'''UPDATE prelim.province
                    SET shape = '{province.geometry().asWkt()}'
                    WHERE province_name = \'{prov}\' 
                 '''
        dbg.exec(query)
    

def insertDistrict(layer):
    names = {
                'Beitbridge': 'Beitbridge Rural',
                'Chiredzi': 'Chiredzi Rural',
                'Masvingo': 'Masvingo Rural',
                'Bindura': 'Bindura Rural',
                'Centenary/ Muzarabani': 'Muzarabani',
                'Hwange': 'Hwange Rural',
                'Chipinge': 'Chipinge Rural',
                'Chegutu': 'Chegutu Rural',
                'Kariba': 'Kariba Rural',
                'Gweru': 'Gweru Rural',
                'Kwekwe': 'Kwekwe Rural',
                'Marondera': 'Marondera Rural',
                'Mutare': 'Mutare Rural',
                'Zvishavane': 'Zvishavane Rural',
                'Shurugwi': 'Shurugwi Rural',
                'Ruwa': 'Ruwa Local Board',
                'Shurugwi Town': 'Shurugwi Urban',
                'Gokwe South Urban': 'Gokwe Centre',
                'Kadoma Urban': 'Kadoma',
                'Chinhoyi': 'Chinhoyi Urban',
                'Harare': 'Harare Urban',
                'Chipinge': 'Chipinge Rural' 
            }
   
    layer.selectAll()
    l = [d.attributes()[2] for d in layer.getSelectedFeatures()]
    
    for district in layer.getSelectedFeatures():
        d = {
                'district_name': district.attributes()[2], 
                'province_name': district.attributes()[7], 
                'shape': district.geometry().asWkt(),
            }
        
        if d['district_name'] in (tuple(names.keys())):
            d['district_name'] = names[d['district_name']]
        
        query = f'''UPDATE prelim.district
                    SET shape = '{district.geometry().asWkt()}'
                    WHERE district_name = \'{d['district_name']}\' 
                 '''
        dbg.exec(query)

def insertWard(layer):
    names = {
                'Beitbridge': 'Beitbridge Rural',
                'Chiredzi': 'Chiredzi Rural',
                'Masvingo': 'Masvingo Rural',
                'Bindura': 'Bindura Rural',
                'Centenary/ Muzarabani': 'Muzarabani',
                'Hwange': 'Hwange Rural',
                'Chipinge': 'Chipinge Rural',
                'Chegutu': 'Chegutu Rural',
                'Kariba': 'Kariba Rural',
                'Gweru': 'Gweru Rural',
                'Kwekwe': 'Kwekwe Rural',
                'Marondera': 'Marondera Rural',
                'Mutare': 'Mutare Rural',
                'Zvishavane': 'Zvishavane Rural',
                'Shurugwi': 'Shurugwi Rural',
                'Ruwa': 'Ruwa Local Board',
                'Shurugwi Town': 'Shurugwi Urban',
                'Gokwe South Urban': 'Gokwe Centre',
                'Kadoma Urban': 'Kadoma',
                'Chinhoyi': 'Chinhoyi Urban',
                'Harare': 'Harare Urban',
                'Chipinge': 'Chipinge Rural' 
            }

    layer.selectAll()
    for ward in layer.getSelectedFeatures():
        district = ward.attributes()[7]
        
        d = {
                'ward_number': ward.attributes()[2],
                'district_name': ward.attributes()[7],
                'province_name': ward.attributes()[9],
                'shape': ward.geometry().asWkt(),
            }
        
        if d['district_name'] in tuple(names.keys()):
            d['district_name'] = names[d['district_name']]
            

        query = f'''UPDATE prelim.ward
                    SET shape = '{ward.geometry().asWkt()}'
                    WHERE district_name = \'{d['district_name']}\'
                    AND ward_number = {d['ward_number']}
                 '''
        dbg.exec(query)


if __name__ == "__main__":
    assert len(sys.argv) == 4
    insertWard(QgsVectorLayer(sys.argv[3]))
    insertDistrict(QgsVectorLayer(sys.argv[2]))
    insertProvince(QgsVectorLayer(sys.argv[1]))


