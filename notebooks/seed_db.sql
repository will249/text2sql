-- Add postGIS extension
CREATE EXTENSION postgis;

-- Cleaned aircraft position data (as PostGIS object) for each minute (datetime) of a flight)
CREATE TABLE aircraft_position_gis (
    flight_id int,
    position geography(POINT, 4326),
    datetime timestamptz,
);

-- Raw aircraft position data for every minute (datetime) of a flight
CREATE TABLE aircraft_position_raw (
      lon float,
      lat float,
      speedMph float,
      altitudeFt int,
      source varchar,
      datetime timestamptz,
      flight_id int
);

-- Aircraft asset details
CREATE TABLE aircraft_assets (
    id int,
    tail_number varchar,
    manufacturer varchar,
    model varchar,
    registration varchar,
    status varchar,
    last_maintenance_date date,
    next_maintenance_date date,
    next_maintenance_miles int,
    next_maintenance_hours int,
    next_maintenance_days int,
);

-- Aircraft historical flights
CREATE TABLE aircraft_historical_flights (
    id int,
    tail_number varchar,
    flight_id varchar,
    departure_airport varchar,
    arrival_airport varchar,
    departure_time timestamptz,
    arrival_time timestamptz,
    duration_miles int,
    duration int,
);

-- Regions of interest
CREATE TABLE regions_of_interest (
    id int,
    name varchar,
    region geography(POLYGON, 4326),
); 

-- Airport locations
CREATE TABLE airport_locations (
    id int,
    name varchar,
    code varchar,
    city varchar,
    country varchar,
    location geography(POINT, 4326),
);

-- Airport runways
CREATE TABLE airport_runways (
    id int,
    airport_id int,
    length int,
    width int,
    surface varchar,
    direction varchar,
);

-- Shipping vehicle asset details 
CREATE TABLE shipping_vehicle_assets (
    id int,
    name varchar,
    type varchar,
    manufacturer varchar,
    model varchar,
    registration varchar,
    status varchar,
    last_maintenance_date date,
    next_maintenance_date date,
    next_maintenance_miles int,
    next_maintenance_hours int,
    next_maintenance_days int,
);

-- Shipping vehicle historical journeys
CREATE TABLE shipping_vehicle_historical_journeys (
    id int,
    shipping_vehicle_id int,
    origin geography(POINT, 4326),
    destination geography(POINT, 4326),
    departure_time timestampz,
    arrival_time timestampz,
    duration_miles int,
    duration_hours int,
    duration_days int,
);

-- Raw shipping vehicle position data 
CREATE TABLE shipping_vehicle_position_raw (
    lon float,
    lat float,
    speedMph float,
    altitudeFt int,
    source varchar,
    date timestampz,
    shipping_vehicle_id int
);

-- Cleaned shipping vehicle position data
CREATE TABLE shipping_vehicle_position_gis (
    position geography(POINT, 4326),
    date timestamptz,
    shipping_vehicle_id int,
);

-- Logistic hub locations
CREATE TABLE logistic_hub_locations (
    id int,
    name varchar,
    location geography(POINT, 4326),
);

-- Transit vehicle asset details 
CREATE TABLE transit_vehicle_assets (
    id int,
    name varchar,
    type varchar,
    manufacturer varchar,
    model varchar,
    registration varchar,
    status varchar,
    last_maintenance_date date,
    next_maintenance_date date,
    next_maintenance_miles int,
    next_maintenance_hours int,
    next_maintenance_days int,
);

-- Transit vehicle historical journeys
CREATE TABLE transit_vehicle_historical_journeys (
    id int,
    transit_vehicle_id int,
    origin geography(POINT, 4326),
    destination geography(POINT, 4326),
    departure_time timestampz,
    arrival_time timestampz,
    duration_miles int,
    duration_hours int,
    duration_days int,
);

-- Raw transit vehicle position data 
CREATE TABLE transit_vehicle_position_raw (
    lon float,
    lat float,
    speedMph float,
    altitudeFt int,
    source varchar,
    date timestampz,
    transit_vehicle_id int
);

-- Cleaned transit vehicle position data
CREATE TABLE transit_vehicle_position_gis (
    position geography(POINT, 4326),
    date timestamptz,
    transit_vehicle_id int,
);






