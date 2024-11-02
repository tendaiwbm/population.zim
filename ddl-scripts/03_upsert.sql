/*
  Created by:	tendaiwbm
  This script serves to perform upserts in 
	1. ward
	2. district
	3. province
  to add
	1. numberofwards
	2. numberofdistricts
	3. area
  where appropriate
*/

---------------------------------------------------------
-- WARD
---------------------------------------------------------
CREATE OR REPLACE FUNCTION prelim.updateWardProvince()
RETURNS void
AS $$
DECLARE
	relation	RECORD;
BEGIN
	FOR relation in 
		SELECT district_name,province_name FROM prelim.district
	LOOP
		UPDATE prelim.ward
		SET province_name = relation.province_name
		WHERE district_name = relation.district_name;
	END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION prelim.updateWardArea()
RETURNS void
AS $$
DECLARE
BEGIN
	UPDATE prelim.ward
	SET area = ST_AREA(shape)/1000000;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION prelim.updateWardDensities()
RETURNS void
AS $$
DECLARE
	row_	RECORD;
	sql_	TEXT := NULL;
BEGIN
	FOR row_ in
		SELECT * FROM (VALUES 
			('male_population_2022','male_population_density_2022'),
			('male_population_2012','male_population_density_2012'),
			('female_population_2022','female_population_density_2022'),
			('female_population_2012','female_population_density_2012'),
			('total_population_2022','total_population_density_2022'),
			('total_population_2012','total_population_density_2012'),
			('total_households_2022','total_households_density_2022'),
			('total_households_2012','total_households_density_2012'))
		AS t(source,density)
	LOOP
		sql_ := concat(sql_,format('UPDATE prelim.ward SET %I = %I/area;',row_.density,row_.source));
	END LOOP;
EXECUTE sql_;
END;
$$ LANGUAGE plpgsql;

-----------------------------------------------------------
-- DISTRICT
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION prelim.updateDistrictNumWards()
RETURNS void
AS $$
DECLARE 
	relation	RECORD;
BEGIN
	FOR relation in
		SELECT district_name from prelim.district
	LOOP
		UPDATE prelim.district
		SET numberofwards = (SELECT COUNT(ward_number) FROM prelim.ward GROUP BY district_name HAVING district_name = relation.district_name)
		WHERE district_name = relation.district_name;
	END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION prelim.updateDistrictArea()
RETURNS void
AS $$
DECLARE
BEGIN
        UPDATE prelim.district
        SET area = ST_AREA(shape)/1000000;
END;    
$$ LANGUAGE plpgsql;


-----------------------------------------------------------
-- PROVINCE
-----------------------------------------------------------
CREATE OR REPLACE FUNCTION prelim.updateProvinceNumWards()
RETURNS void
AS $$
DECLARE
	relation	RECORD;
BEGIN
	FOR relation in
		SELECT province_name from prelim.district
	LOOP
		UPDATE prelim.province
		SET numberofwards = (SELECT SUM(numberofwards) FROM prelim.district GROUP BY province_name HAVING province_name = relation.province_name)
		WHERE province_name = relation.province_name;
	END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION prelim.updateProvinceNumDistricts()
RETURNS void
AS $$
DECLARE
	relation	RECORD;
BEGIN
	FOR relation in
		SELECT province_name FROM prelim.province
	LOOP
		UPDATE prelim.province
		SET numberofdistricts = (SELECT COUNT(district_name) FROM prelim.district GROUP BY province_name HAVING province_name = relation.province_name)
		WHERE province_name = relation.province_name;
	END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION prelim.updateProvinceArea()
RETURNS void
AS $$
DECLARE
BEGIN
        UPDATE prelim.province
        SET area = ST_AREA(shape)/1000000;
END;
$$ LANGUAGE plpgsql;

------------------------------------
-- EXEC
------------------------------------
SELECT prelim.updateWardProvince();
SELECT prelim.updateWardArea();
SELECT prelim.updateWardDensities();
SELECT prelim.updateDistrictNumWards();
SELECT prelim.updateDistrictArea();
SELECT prelim.updateProvinceNumWards();
SELECT prelim.updateProvinceNumDistricts();
SELECT prelim.updateProvinceArea();




