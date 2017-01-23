
CREATE TABLE users(
user_pk serial not null, 
username text not null,
active boolean not null,
PRIMARY KEY(user_pk));

CREATE TABLE roles(
role_pk serial not null,
title text not null,
PRIMARY KEY(role_pk));

CREATE TABLE user_is(
user_fk int not null,
role_fk int not null);

CREATE TABLE user_supports(
user_fk int not null,
facility_fk int not null);

CREATE TABLE products(
product_pk serial not null,
vendor text,
description text,
alt_description text, 
PRIMARY KEY(product_pk));

CREATE TABLE assets(
asset_pk serial not null, 
product_fk int not null,
asset_tag text not null,
description text,
alt_description text,
PRIMARY KEY(asset_pk));

CREATE TABLE vehicles(
vehicle_pk serial not null,
asset_fk int,
PRIMARY KEY(vehicle_pk)); 

CREATE TABLE facilities(
facility_pk serial not null,
fcode text not null,
common_name text not null,
location text,
PRIMARY KEY(facility_pk));

CREATE TABLE asset_at(
asset_fk int not null,
facility_fk int not null,
arrive_dt timestamp,
depart_dt timestamp);

CREATE TABLE convoys(
convoy_pk serial not null,
request text not null,
source_fk int not null,
dest_fk int not null,
depart_dt timestamp,
arrive_dt timestamp,
PRIMARY KEY(convoy_pk));

CREATE TABLE used_by(
vehicle_fk int not null,
convoy_fk int not null);

CREATE TABLE asset_on(
asset_fk int not null,
convoy_fk int not null,
load_dt timestamp,
unload_dt timestamp);

CREATE TABLE levels(
level_pk serial not null,
abbrv text not null,
comment text,
PRIMARY KEY(level_pk));

CREATE TABLE compartments(
compartment_pk serial not null,
abbrv text not null,
comment text,
PRIMARY KEY(compartment_pk));

CREATE TABLE security_tags(
tag_pk serial not null,
level_fk int not null,
compartment_fk int not null,
user_fk int,
product_fk int,
asset_fk int);
