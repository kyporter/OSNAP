
CREATE TABLE users(
user_pk serial,
username varchar(16) NOT NULL UNIQUE,
password varchar(16) NOT NULL,
active boolean NOT NULL DEFAULT 1,
PRIMARY KEY(user_pk));
