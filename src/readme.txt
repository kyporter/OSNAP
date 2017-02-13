**IMPORTANT! config.py reads in from lost_pub key file: if lost_config.json is pointing to a 
file that doesn't exist for lost_pub, it will raise an error. After running preflight.sh, there 
will be a lost.pub file in src that by default lost_config.json is pointing to.

All database-related API calls will interact with the database

app.py : makes things work with wsgi
config.py: reads in data from lost_config.json, translates it to python variables
lost_config.json: stores configuration information

templates folder:
  contains .html to give pages content
  -login.html: the login page, username and password sent to ...
  -report_main.html: the basecamp page for all things report-related, might send things to ...
      -facility_report.html: the page with the facility inventory: displays a table with asset information for a given date and facility
  -report_main.html may also send to ...
      -transit_report.html: the page with the traveling asset info for a given date: displays a table with asset and facility information
  -logout.html: the goodbye page, with a link back around to ... the login page!
  
  -rest.html: displays API calls and their parameters

Can be run directly from wsgi (apachectl start and the pages are good to go!)
