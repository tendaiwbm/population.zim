DROP DATABASE IF EXISTS "populationZim";
CREATE DATABASE "populationZim" OWNER tendaiwbm;
\c populationZim
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE SCHEMA prelim;

CREATE TABLE prelim.boundary_enumerations (
	id SERIAL PRIMARY KEY,
        enum_class VARCHAR(15) NOT NULL,
	enum_value VARCHAR(50) NOT NULL
);

CREATE TABLE prelim.province (
	province_name VARCHAR(20) PRIMARY KEY,
	numberofdistricts INTEGER,
	numberofwards INTEGER,
	area NUMERIC,
	shape GEOGRAPHY(MULTIPOLYGON,4326)
);

CREATE TABLE prelim.district (
	district_name VARCHAR(30) PRIMARY KEY,
	numberofwards INTEGER,
	province_name VARCHAR(30) references prelim.province(province_name),
	area NUMERIC,
	shape GEOGRAPHY(MULTIPOLYGON,4326)
);

CREATE TABLE prelim.ward (
	ward_number INTEGER NOT NULL,
	district_name VARCHAR(30) references prelim.district(district_name),
	province_name VARCHAR(30) references prelim.province(province_name),
	male_population_2022 INTEGER NOT NULL,
	male_population_density_2022 INTEGER,
	female_population_2022 INTEGER NOT NULL,
	female_population_density_2022 INTEGER,
	total_population_2022 INTEGER NOT NULL CHECK(total_population_2022 = female_population_2022 + male_population_2022),
	total_population_density_2022 INTEGER,
	male_population_2012 INTEGER NOT NULL,
	male_population_density_2012 INTEGER,
	female_population_2012 INTEGER NOT NULL,
	female_population_density_2012 INTEGER,
	total_population_2012 INTEGER NOT NULL CHECK(total_population_2012 = female_population_2012 + male_population_2012),
	total_population_density_2012 INTEGER,
	total_households_2022 INTEGER NOT NULL,
	total_households_density_2022 INTEGER,
	avg_householdsize_2022 NUMERIC(3,1) NOT NULL CHECK(avg_householdsize_2022 = ROUND((total_population_2022/total_households_2022::NUMERIC),1)),
	total_households_2012 INTEGER NOT NULL,
	total_households_density_2012 INTEGER,
	avg_householdsize_2012 NUMERIC(3,1) NOT NULL CHECK(avg_householdsize_2012 = ROUND((total_population_2012/total_households_2012::NUMERIC),1)),
	area NUMERIC,
	shape GEOGRAPHY(MULTIPOLYGON,4326),
	PRIMARY KEY(ward_number,district_name)
);

REVOKE ALL ON SCHEMA "prelim" FROM PUBLIC;
REVOKE ALL ON DATABASE "populationZim" FROM PUBLIC;
