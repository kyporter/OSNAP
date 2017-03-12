
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
acq_date timestamp, --improves logic of import/export action
PRIMARY KEY(asset_pk));

CREATE TABLE facilities(
facility_pk serial,
common_name varchar(32), 
fac_code varchar(6),
PRIMARY KEY(facility_pk));

CREATE TABLE asset_history( 
asset_fk integer NOT NULL,
facility_fk integer,
arrive_dt timestamp NOT NULL,
depart_dt timestamp);

--Originally had transfer requests and load info separate, but there really isn't a good reason to
--Since a given transfer request can only have one set of load/unload info associated with it(and vice versa)
CREATE TABLE transfer_requests(
request_pk serial,
requester integer REFERENCES users,
req_time timestamp,
source integer REFERENCES facilities,
destination integer REFERENCES facilities,
asset_fk integer,
approver integer REFERENCES users,
app_time timestamp,
load_dt timestamp,
unload_dt timestamp,
sets_load integer REFERENCES users,
sets_unload integer REFERENCES users,
PRIMARY KEY(request_pk));


--Because two roles are assumed to exist:
INSERT INTO roles (title, description) VALUES ('Logistics Officer', 'May dispose 
of assets');

INSERT INTO roles(title) VALUES ('Facilities Officer');

--For functionality/thoroughness in asset_history:
INSERT INTO facilities (common_name, fac_code) VALUES ('in transit', 'INTRAN');
