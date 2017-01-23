CREATE TABLE users(user_pk serial not null,username text not null,active boolean not null,PRIMARY KEY(user_pk));
CREATE TABLE user_is(user_fk int not null,role_fk int not null);
CREATE TABLE user_supports(user_fk int not null,facility_fk int not null);
