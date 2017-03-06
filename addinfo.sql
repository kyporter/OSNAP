INSERT INTO users (username, password, role_fk) VALUES ('Timmy', 'southpark', 1);
INSERT INTO users (username, password, role_fk) VALUES ('Kenny', 'southpark', 2);
INSERT INTO users (username, password, role_fk) VALUES ('Stan', 'southpark', 1);
INSERT INTO users (username, password, role_fk) VALUES ('Cartman', 'southpark', 
2);
INSERT INTO users (username, password, role_fk) VALUES ('Kyle', 'southpark', 1);
INSERT INTO users (username, password, role_fk) VALUES ('Towelie', 'southpark', 
2);
INSERT INTO users (username, password, role_fk) VALUES ('Garrison', 'southpark', 
1);
INSERT INTO users (username, password, role_fk) VALUES ('Manbearpig', 'southpark', 
2);

INSERT INTO assets (asset_tag, description) VALUES ('123456', 'Chocolate Frogs'); 
INSERT INTO assets (asset_tag, description) VALUES ('234567', 'Chocolate Bunnies'); 
INSERT INTO assets (asset_tag, description) VALUES ('345678', 'Chocolate Snow'); 
INSERT INTO assets (asset_tag, description) VALUES ('456789', 'Keyboard'); 
INSERT INTO assets (asset_tag, description) VALUES ('567890', 'Mouse'); 
INSERT INTO assets (asset_tag, description) VALUES ('HOTSHOT', 'Monitor'); 
INSERT INTO assets (asset_tag, description) VALUES ('TANGOF', 'Whiskey'); 
INSERT INTO assets (asset_tag, description) VALUES ('ALPHA1', '2 TB RAM'); 
INSERT INTO assets (asset_tag, description) VALUES ('POIUYT', 'xBox One'); 
INSERT INTO assets (asset_tag, description) VALUES ('ASDFGH', 'Desk'); 
INSERT INTO assets (asset_tag, description) VALUES ('QWERTY', 'Chair'); 

INSERT INTO FACILITIES (common_name, fac_code) VALUES ('Washington, D.C.', 'DC');
INSERT INTO FACILITIES (common_name, fac_code) VALUES ('Headquarters', 'HQ');
INSERT INTO FACILITIES (common_name, fac_code) VALUES ('Los Alamos, New Mexico', 'LANM');
INSERT INTO FACILITIES (common_name, fac_code) VALUES ('Los Angeles', 'LA');
INSERT INTO FACILITIES (common_name, fac_code) VALUES ('New York City', 'NYC');
INSERT INTO FACILITIES (common_name, fac_code) VALUES ('Rome, Texas', 'ROME');

INSERT INTO asset_history(asset_fk, facility_fk, arrive_dt) VALUES (1, 4, '3/1/16');
INSERT INTO asset_history(asset_fk, facility_fk, arrive_dt) VALUES (2, 2, 
'2/1/17');
INSERT INTO asset_history(asset_fk, facility_fk, arrive_dt) VALUES (3, 3, 
'3/1/16');
INSERT INTO asset_history(asset_fk, facility_fk, arrive_dt) VALUES (4, 6, 
'2/1/16');
INSERT INTO asset_history(asset_fk, facility_fk, arrive_dt) VALUES (5, 1, 
'3/2/16');
INSERT INTO asset_history(asset_fk, facility_fk, arrive_dt) VALUES (6, 5, 
'3/1/16');
INSERT INTO asset_history(asset_fk, facility_fk, arrive_dt) VALUES (7, 4, 
'3/14/15');
INSERT INTO asset_history(asset_fk, facility_fk, arrive_dt) VALUES (8, 1, 
'12/1/16');
INSERT INTO asset_history(asset_fk, facility_fk, arrive_dt) VALUES (9, 1, 
'3/1/17');
INSERT INTO asset_history(asset_fk, facility_fk, arrive_dt) VALUES (10, 5, 
'2/11/17');
INSERT INTO asset_history(asset_fk, facility_fk, arrive_dt) VALUES (11, 3, 
'1/1/16');
