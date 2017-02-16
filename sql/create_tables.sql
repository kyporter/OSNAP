
CREATE TABLE users(
user_pk serial,
username varchar(16) NOT NULL UNIQUE, /*for now, I'm using a numeric primary key because I read that 
sql handles integers better and it is recommended to use numeric over text primary keys*/
password varchar(16) NOT NULL, /*for now, I'm using the 16 character limit from the spec for a 
plaintext password*/
active boolean NOT NULL DEFAULT True, /*I figure eventually we'll want this value, and it's easy to 
set up, so I put it in now*/
PRIMARY KEY(user_pk));
