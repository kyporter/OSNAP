app.py : makes things work with wsgi: creates routes and defines behavior of routes
config.py: reads in data from lost_config.json, translates it to python variables(only requires dbname, dbhost and dbport)
lost_config.json: stores configuration information

templates folder:
  contains .html to give pages content
  -create_user.html: renders create user page, sends username, password and role to database; if successful, directs to c_user_success.html, else directs to c_user_fail.html
  -c_user_success.html: announces success of user creation and provides link to login page
  -c_user_fail.html: announces failure of user creation and provides link to create user page
  -login.html: the login page, username and password sent to dashboard.html if successful; to login_fail.html if not
  -dashboard.html: currently displays logged in user's name, role; provides links to add_asset, add_facility, asset_report and logout; if user is a logistics officer, provides link to dispose_asset
  -login_fail.html: announces failure of login and provides link back to login page
  -add_asset.html: displays list of asset tags/descriptions currently in database and form to add new asset; provides links to dashboard and logout
  -add_ast_fail.html: announces failure to add asset and provides link back to add_asset page
  -add_facility.html: displays form to add new facility; directs to add_fac_fail.html if adding fails; provides links to dashboard and logout
  -add_fac_fail.html: announces failure to add facility and provides link back to add_facility page
  -LO_only.html: displays if non-logistics officers try to access dispose_asset; provides links to dashboard and logout
  -disposal_form.html: displays only if user is logistics officer; displays form to dispose of asset; disposal success links back to same .html; failure leads to already_disposed.html or no_asset.html; provides links to dashboard and logout
  -already_disposed.html: displays if asset being disposed of was already disposed of(based on database state, not date); provides link back to dispose_asset page
  -no_asset.html: displays if asset being disposed of does not exist in database; provides link back to dispose_asset page
  -g_report_request.html: displays on 'GET' method request to asset_report; only displays form to make report request
  -p_report_request.html: displays on 'POST' method request to asset_report; displays form for report request and table displaying last requested info
  -logout.html: displays goodbye message on session end; provides link to login page



Can be run directly from wsgi (apachectl start and the pages are good to go!)
