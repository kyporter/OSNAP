import csv
with open('./osnap_legacy/transit.csv', 'r') as f:
	reader = csv.reader(f)
	firstline = True
	for row in reader:
		if firstline:
			next
		else:
			word1 = row[0]
			word1.strip('"')
			assets = word1.split(',')		
			for item in assets:
				print(str.format("INSERT INTO assets (asset_tag) SELECT '{}' WHERE NOT EXISTS (SELECT asset_tag FROM assets WHERE asset_tag = '{}');", item, item))
				
			row[1] = row[1].strip('"')
			if row[1] == "Los Alamous, NM":
				row[1] = "Los Alamos, NM"
			elif row[1] == "Las Alamos, NM":
				row[1] = "Los Alamos, NM"
			for i in range(1,3):
				print(str.format("INSERT INTO facilities (common_name) SELECT '{}' WHERE NOT EXISTS (SELECT common_name FROM facilities WHERE common_name = '{}');", row[i], row[i]))   
			print(str.format("INSERT INTO convoys (request,depart_dt,arrive_dt,source_fk,dest_fk) VALUES ((SELECT '{}' WHERE NOT EXISTS (SELECT request FROM convoys WHERE request = '{}')),('{}' WHERE NOT EXISTS (SELECT request FROM convoys WHERE request = '{}')),('{}' WHERE NOT EXISTS (SELECT request FROM convoys WHERE request = '{}')),(SELECT facility_pk FROM facilities WHERE common_name='{}' WHERE NOT EXISTS (SELECT request FROM convoys WHERE request = '{}')),(SELECT facility_pk FROM facilities WHERE common_name='{}' WHERE NOT EXISTS (SELECT request FROM convoys WHERE request = '{}')));", row[5],row[5],row[3],row[5],row[4],row[5], row[1],row[5], row[2],row[5]))

			for item in assets:
					print(str.format("INSERT INTO asset_at (asset_fk, facility_fk,arrive_dt) VALUES ((SELECT asset_pk FROM assets WHERE asset_tag='{}'), (SELECT facility_pk FROM facilities WHERE common_name='{}'),'{}');",item,row[2],row[4]))
		firstline = False 
f.close()

with open('./osnap_legacy/DC_inventory.csv', 'r') as f:
	reader = csv.reader(f)
	firstline = True
	for row in reader:
		if firstline:
			next
		else:
			comptag = row[3].split(":")
			print(str.format("INSERT INTO assets (asset_tag) SELECT '{}' WHERE NOT EXISTS (SELECT asset_tag FROM assets WHERE asset_tag='{}');", row[0], row[0]))
			print(str.format("INSERT INTO products (description) SELECT '{}' WHERE NOT EXISTS (SELECT description FROM products WHERE description='{}');",row[1],row[1]))
			print(str.format("INSERT INTO compartments (abbrv) SELECT '{}' WHERE NOT EXISTS (SELECT abbrv FROM compartments WHERE abbrv='{}');",comptag[0],comptag[0]))
			
		firstline = False
f.close()
