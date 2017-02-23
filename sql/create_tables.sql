
CREATE TABLE users(
user_pk serial,
username varchar(16) NOT NULL UNIQUE, /*for now, I'm using a numeric primary key because I read that 
sql handles integers better and it is recommended to use numeric over text primary keys*/
password varchar(16) NOT NULL, /*for now, I'm using the 16 character limit from the spec for a 
plaintext password*/
active boolean NOT NULL DEFAULT True, /*I figure eventually we'll want this value, and it's easy to 
set up, so I put it in now*/
role_fk integer,
PRIMARY KEY(user_pk));

CREATE TABLE roles(
role_pk serial,
title varchar(40) NOT NULL, --this should allow reasonable-length titles
description text, --gives a place to specify permissions and duties
PRIMARY KEY(role_pk));

CREATE TABLE assets(
asset_pk serial,
asset_tag varchar(16) NOT NULL,
description text, --I really want this to be not null but for now I'll leave it nullable
PRIMARY KEY(asset_pk));

CREATE TABLE facilities(
facility_pk serial,
common_name varchar(32), 
fac_code varchar(6),
PRIMARY KEY(facility_pk));

CREATE TABLE asset_history( --still deciding if I want to have a currently at table as well or if that's too redundant
asset_fk integer NOT NULL,
facility_fk integer,
arrive_dt timestamp NOT NULL,
depart_dt timestamp);

--Because two roles are assumed to exist:
INSERT INTO roles (title, description) VALUES ('Logistics Officer', 'May dispose 
of assets');

INSERT INTO roles(title) VALUES ('Facilities Officer');
