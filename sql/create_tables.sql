
CREATE TABLE users(
user_pk serial not null, 
username text not null,
active boolean not null,
PRIMARY KEY(user_pk));

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
