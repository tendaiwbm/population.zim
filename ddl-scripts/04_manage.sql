CREATE INDEX ward_geom_idx ON prelim.ward USING GIST (shape);
CREATE INDEX district_geom_idx ON prelim.district USING GIST (shape);
CREATE INDEX province_geom_idx ON prelim.province USING GIST (shape);

--------------------------------------------------------------------------------
-- TRIGGER FUNCTION INSERT ON province
--------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_ins_province() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_ins_province()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'INSERT not permitted';
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_ins_province() FROM PUBLIC;

-------------------------------------------------------------------------------
-- TRIGGER FUNCTION UPDATE ON province
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_upd_province() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_upd_province()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'UPDATE not permitted';
RETURN NULL;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_upd_province() FROM PUBLIC;

-------------------------------------------------------------------------------
-- TRIGGER FUNCTION DELETE ON province
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_del_province() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_del_province()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'DELETE not permitted';
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_del_province() FROM PUBLIC;

-------------------------------------------------------------------------------
-- TRIGGER FUNCTION TRUNCATE ON province
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_trunc_province() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_trunc_province()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'TRUNCATE not permitted';
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_trunc_province() FROM PUBLIC;

-------------------------------------------------------------------------------
-- TRIGGER FUNCTION INSERT ON district
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_ins_district() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_ins_district()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'INSERT not permitted';
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_ins_district() FROM PUBLIC;

-------------------------------------------------------------------------------
-- TRIGGER FUNCTION UPDATE ON district
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_upd_district() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_upd_district()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'UPDATE not permitted';
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_upd_district() FROM PUBLIC;

-------------------------------------------------------------------------------
-- TRIGGER FUNCTION DELETE ON district
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_del_district() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_del_district()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'DELETE not permitted';
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_del_district() FROM PUBLIC;

-------------------------------------------------------------------------------
-- TRIGGER FUNCTION TRUNCATE ON district
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_trunc_district() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_trunc_district()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'TRUNCATE not permitted';
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_trunc_district() FROM PUBLIC;

-------------------------------------------------------------------------------
-- TRIGGER FUNCTION INSERT ON ward
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_ins_ward() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_ins_ward()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'INSERT not permitted';
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_ins_ward() FROM PUBLIC;

-------------------------------------------------------------------------------
-- TRIGGER FUNCTION UPDATE ON ward
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_upd_ward() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_upd_ward()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'UPDATE not permitted';
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_upd_ward() FROM PUBLIC;

-------------------------------------------------------------------------------
-- TRIGGER FUNCTION DELETE ON ward
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_del_ward() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_del_ward()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'DELETE not permitted';
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_del_ward() FROM PUBLIC;

-------------------------------------------------------------------------------
-- TRIGGER FUNCTION TRUNCATE ON ward
-------------------------------------------------------------------------------
DROP FUNCTION IF EXISTS prelim.tr_trunc_ward() CASCADE;
CREATE OR REPLACE FUNCTION prelim.tr_trunc_ward()
RETURNS trigger
AS $$
DECLARE
BEGIN
	RAISE EXCEPTION 'TRUNCATE not permitted';
RETURN OLD;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.tr_del_ward() FROM PUBLIC;



DROP FUNCTION IF EXISTS prelim.generate_sql_triggers() CASCADE;
CREATE OR REPLACE FUNCTION prelim.generate_sql_triggers()
RETURNS INTEGER 
AS $$
DECLARE 
relation	RECORD;
tr		RECORD;
trigger_f	VARCHAR;
trigger_n	VARCHAR;
sql_trig	TEXT := NULL;
sql_statement	TEXT := NULL;

BEGIN
	FOR relation in
		SELECT * FROM (VALUES
			('province'),
			('district'),
			('ward'))
		AS r(admin)
	LOOP
		FOR tr in 
			SELECT * FROM (VALUES
				('ins','INSERT'),
				('upd','UPDATE'),
				('del','DELETE'))
			AS t(prefix,task)
		LOOP
			trigger_f := format('tr_%s_%s()',tr.prefix,relation.admin);
			trigger_n := concat('tr_',tr.prefix,'_',relation.admin);
			sql_trig := NULL;
			sql_trig := format('
				DROP TRIGGER IF EXISTS %I ON prelim.%I;
				CREATE TRIGGER %I
				BEFORE %s ON prelim.%I
				FOR EACH ROW EXECUTE FUNCTION prelim.%s;
				COMMENT ON TRIGGER %I ON prelim.%I IS ''Tripped on %s into relation prelim.%I'';',
				trigger_n,relation.admin,trigger_n,tr.task,relation.admin,trigger_f,
				trigger_n,relation.admin,tr.task,relation.admin);
			sql_statement := concat(sql_statement,sql_trig);
		END LOOP;
	END LOOP;
EXECUTE sql_statement;
RETURN 1;
END;
$$ LANGUAGE plpgsql;
REVOKE EXECUTE ON FUNCTION prelim.generate_sql_triggers() FROM PUBLIC;

SELECT prelim.generate_sql_triggers();


