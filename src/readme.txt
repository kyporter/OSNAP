app.py : makes things work with wsgi: creates routes and defines behavior of routes
Current routes:
	/ and /login(equivalent): initiates session
	/create_user
	/dashboard
	/add_facility
	/add_asset
	/dispose_asset: must be logged in as Logistics Officer
	/asset_report
	/transfer_req: must be logged in as Logistics Officer
	/approve_req: must be logged in as Facilities Officer
	/update_transit: must be logged in as Logistics Officer
	/transfer_report
	/logout: ends session
config.py: reads in data from lost_config.json, translates it to python variables(only requires dbname, dbhost and dbport)
lost_config.json: stores configuration information

templates folder: contains html to display routes; descriptions in templates/readme.txt

Can be run directly from wsgi (apachectl start and the pages are good to go!)
