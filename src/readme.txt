app.py : makes things work with wsgi
config.py: reads in data from lost_config.json, translates it to python variables
lost_config.json: stores configuration information

templates folder:
  contains .html to give pages content
  -create_user.html: renders create user page, sends username and password to database; if successful, directs to 
  c_user_success.html, else directs to c_user_fail.html
  -c_user_success.html: announces success of user creation and provides link to login page
  -c_user_fail.html: announces failure of user creation and provides link to create user page
  -login.html: the login page, username and password sent to dashboard.html if successful; to login_fail.html if not
  -dashboard.html: currently displays logged in user's name
  -login_fail.html: announces failure of login and provides link back to login page

Can be run directly from wsgi (apachectl start and the pages are good to go!)
