app.py : makes things work with wsgi: creates routes and defines behavior of routes
config.py: reads in data from lost_config.json, translates it to python variables(only requires dbname, dbhost and dbport)
lost_config.json: stores configuration information

templates folder: contains html to display routes; descriptions in templates/readme.txt

Can be run directly from wsgi (apachectl start and the pages are good to go!)
