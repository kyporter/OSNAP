
CREATE TABLE users(
user_pk serial, 
username text,
active boolean,
PRIMARY KEY(user_pk));

CREATE TABLE roles(
role_pk serial,
title text,
PRIMARY KEY(role_pk));

CREATE TABLE user_is(
user_fk int,
role_fk int);

CREATE TABLE user_supports(
user_fk int,
facility_fk int);

CREATE TABLE products(
product_pk serial,
vendor text,
description text,
alt_description text, 
PRIMARY KEY(product_pk));

CREATE TABLE assets(
asset_pk serial, 
product_fk int,
asset_tag text,
description text,
alt_description text,
PRIMARY KEY(asset_pk));

CREATE TABLE vehicles(
vehicle_pk serial,
asset_fk int,
PRIMARY KEY(vehicle_pk)); 

CREATE TABLE facilities(
facility_pk serial,
fcode text,
common_name text,
location text,
PRIMARY KEY(facility_pk));

CREATE TABLE asset_at(
asset_fk int,
facility_fk int,
arrive_dt timestamp,
depart_dt timestamp);

CREATE TABLE convoys(
convoy_pk serial,
request text,
source_fk int,
dest_fk int,
depart_dt timestamp,
arrive_dt timestamp,
PRIMARY KEY(convoy_pk));

CREATE TABLE used_by(
vehicle_fk int,
convoy_fk int);

CREATE TABLE asset_on(
asset_fk int,
convoy_fk int,
load_dt timestamp,
unload_dt timestamp);

CREATE TABLE levels(
level_pk serial,
abbrv text,
comment text,
PRIMARY KEY(level_pk));

CREATE TABLE compartments(
compartment_pk serial,
abbrv text,
comment text,
PRIMARY KEY(compartment_pk));

CREATE TABLE security_tags(
tag_pk serial,
level_fk int,
compartment_fk int,
user_fk int,
product_fk int,
asset_fk int);
