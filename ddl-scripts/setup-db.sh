psql -U tendaiwbm -f 01_principal.sql
psql -U tendaiwbm -d populationZim -f 02_insert.sql
python3 03_insert.py /media/sf_shared/ade/data/province/zwe_admbnda_adm1_zimstat_ocha_20180911.shp /media/sf_shared/ade/data/district/zwe_admbnda_adm2_zimstat_ocha_20180911.shp /media/sf_shared/ade/data/ward/zwe_admbnda_adm3_zimstat_ocha_20180911.shp
python3 03_resolve-insert.py /media/sf_shared/ade/data/district/zwe_admbnda_adm2_zimstat_ocha_20180911.shp
psql -U tendaiwbm -d populationZim -f 03_upsert.sql
python3 03_upsert.py
psql -U tendaiwbm -d populationZim -f 04_manage.sql
