app.py : makes things work with wsgi

templates folder:
  contains .html to give pages content
  -login.html: the login page, username and password sent to ...
  -report_main.html: the basecamp page for all things report-related, might send things to ...
      -facility_report.html: the page with the facility inventory
  -report_main.html may also send to ...
      -transit_report.html: the page with the traveling asset info for a given date
  -logout.html: the goodbye page, with a link back around to ... the login page!
