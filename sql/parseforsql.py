import csv
with open('./osnap_legacy/transit.csv', 'r') as f:
	reader = csv.reader(f)
	firstline = True
	request_numbers = []
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
			if row[5] not in request_numbers:
				request_numbers.append(row[5])
				print(str.format("INSERT INTO convoys (request,depart_dt,arrive_dt,source_fk,dest_fk) VALUES (('{}'),('{}'),('{}'),(SELECT facility_pk FROM facilities WHERE common_name='{}' ),(SELECT facility_pk FROM facilities WHERE common_name='{}' ));", row[5], row[3], row[4], row[1], row[2]))

			for item in assets:
					print(str.format("INSERT INTO asset_at (asset_fk, facility_fk,arrive_dt) VALUES ((SELECT asset_pk FROM assets WHERE asset_tag='{}'), (SELECT facility_pk FROM facilities WHERE common_name='{}'),'{}');",item,row[2],row[4]))
		firstline = False 
f.close()


with open('./osnap_legacy/security_levels.csv', 'r') as f:
	reader = csv.reader(f)
	firstline = True
	for row in reader:
		if firstline:
			next
		else:
			print(str.format("INSERT INTO levels (abbrv, comment) VALUES ('{}', '{}');", row[0], row[1]))
		firstline = False
f.close()


with open('./osnap_legacy/security_compartments.csv', 'r') as f:
	reader = csv.reader(f)
	firstline = True
	for row in reader:
		if firstline:
			next
		else:
			print(str.format("INSERT INTO compartments (abbrv, comment) VALUES ('{}', '{}');", row[0], row[1]))
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
			print(str.format("INSERT INTO products (description) SELECT '{}' WHERE NOT EXISTS (SELECT description FROM products WHERE description='{}');",row[1],row[1]))
			print(str.format("INSERT INTO assets (asset_tag,product_fk) SELECT '{}', (SELECT product_pk FROM products WHERE description='{}')  WHERE NOT EXISTS (SELECT asset_tag FROM assets WHERE asset_tag='{}');", row[0], row[1], row[0]))
			print(str.format("INSERT INTO security_tags (level_fk, compartment_fk, product_fk) VALUES ((SELECT level_pk FROM levels WHERE abbrv='{}'),(SELECT compartment_pk FROM compartments WHERE abbrv='{}'),(SELECT product_pk FROM products WHERE description='{}'));", comptag[1],comptag[0],row[1]))
			print(str.format("INSERT INTO security_tags (level_fk, compartment_fk, asset_fk) VALUES ((SELECT level_pk FROM levels WHERE abbrv='{}'),(SELECT compartment_pk FROM compartments WHERE abbrv='{}'),(SELECT asset_pk FROM assets WHERE asset_tag='{}'));", comptag[1],comptag[0],row[0]))

		firstline = False
f.close()


with open('./osnap_legacy/HQ_inventory.csv', 'r') as f:
	reader = csv.reader(f)
	firstline = True
	product_desc = []
	for row in reader:
		if firstline:
			next
		else:
			comptag = row[3].split(":")	
			print(str.format("INSERT INTO products (description) SELECT '{}' WHERE NOT EXISTS (SELECT description FROM products WHERE description='{}');",row[1],row[1]))
			print(str.format("INSERT INTO assets (asset_tag,product_fk) SELECT '{}', (SELECT product_pk FROM products WHERE description='{}')  WHERE NOT EXISTS (SELECT asset_tag FROM assets WHERE asset_tag='{}');", row[0], row[1], row[0]))
			if row[1] not in product_desc:
				product_desc.append(row[1])
				print(str.format("INSERT INTO security_tags (level_fk, compartment_fk, product_fk) VALUES ((SELECT level_pk FROM levels WHERE abbrv='{}'),(SELECT compartment_pk FROM compartments WHERE abbrv='{}'),(SELECT product_pk FROM products WHERE description='{}'));", comptag[1],comptag[0],row[1]))
			print(str.format("INSERT INTO security_tags (level_fk, compartment_fk, asset_fk) VALUES ((SELECT level_pk FROM levels WHERE abbrv='{}'),(SELECT compartment_pk FROM compartments WHERE abbrv='{}'),(SELECT asset_pk FROM assets WHERE asset_tag='{}'));", comptag[1],comptag[0],row[0]))
		firstline = False
f.close()


with open('./osnap_legacy/NC_inventory.csv', 'r') as f:
	reader = csv.reader(f)
	firstline = True
	for row in reader:
		if firstline:
			next
		else:
			print(str.format("INSERT INTO products (description) SELECT '{}' WHERE NOT EXISTS (SELECT description FROM products WHERE description='{}');",row[1],row[1]))
			print(str.format("INSERT INTO assets (asset_tag,product_fk) SELECT '{}', (SELECT product_pk FROM products WHERE description='{}')  WHERE NOT EXISTS (SELECT asset_tag FROM assets WHERE asset_tag='{}');", row[0], row[1], row[0]))
			if row[3] != '':
				comptag = row[3].split(":")
				print(str.format("INSERT INTO security_tags (level_fk, compartment_fk, asset_fk) VALUES ((SELECT level_pk FROM levels WHERE abbrv='{}'),(SELECT compartment_pk FROM compartments WHERE abbrv='{}'),(SELECT asset_pk FROM assets WHERE asset_tag='{}'));", comptag[1],comptag[0],row[0]))
				print(str.format("INSERT INTO security_tags (level_fk, compartment_fk, product_fk) VALUES ((SELECT level_pk FROM levels WHERE abbrv='{}'),(SELECT compartment_pk FROM compartments WHERE abbrv='{}'),(SELECT product_pk FROM products WHERE description='{}'));", comptag[1],comptag[0],row[1]))
		firstline = False
f.close()


with open('./osnap_legacy/MB005_inventory.csv', 'r') as f:
	reader = csv.reader(f)
	firstline = True
	for row in reader:
		if firstline:
			next
		else:
			print(str.format("INSERT INTO products (description) SELECT '{}' WHERE NOT EXISTS (SELECT description FROM products WHERE description='{}');",row[1],row[1]))
			print(str.format("INSERT INTO assets (asset_tag,product_fk) SELECT '{}', (SELECT product_pk FROM products WHERE description='{}')  WHERE NOT EXISTS (SELECT asset_tag FROM assets WHERE asset_tag='{}');", row[0], row[1], row[0]))
			print(str.format("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES ((SELECT asset_pk FROM assets WHERE asset_tag = '{}'),(SELECT facility_pk FROM facilities WHERE common_name='MB 005'), '12/15/16');", row[0]))			
		firstline = False
f.close()
