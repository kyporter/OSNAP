  contains .html to give pages content
  -create_user.html: renders create user page, POSTs username, password and role to /create_user
  -c_user_success.html: takes username as 'username', announces success of user creation and provides link to login page
  -c_user_fail.html: takes username as 'username', announces failure of user creation and provides link to create user page
  -login.html: the login page, username and password POSTed to /login
  -dashboard.html: takes username as 'username' and role as 'role', displays logged in user's name and role; provides links 
to add_asset, add_facility, asset_report and logout; if user is a logistics officer, provides link to dispose_asset
  -login_fail.html: announces failure of login and provides link back to login page
  -add_asset.html: takes list of asset lists(item[0] as asset_tag, item[1] as description) as 'assets' and list of 
facility lists(item[0] as common name, item[1] as facility code) as 'faclist', displays list of asset 
tags/descriptions currently in database and the form to add new asset; form info POSTs to /add_asset; provides links 
to dashboard and logout
  -add_ast_fail.html: takes asset tag as 'asset', announces failure to add asset and provides link back to add_asset page
  -add_facility.html: takes list of facility lists(item[0] as common name, item[1] as facility code) as 'faclist', 
displays list of facility common names/codes and the form to add new facility; POSTs form information to /add_facility, 
provides links to dashboard and logout
  -add_fac_fail.html: takes facility common name as 'c_name', announces failure to add facility and provides link 
back to add_facility page
  -LO_only.html: displays if non-logistics officers try to access dispose_asset; provides links to dashboard and logout
  -disposal_form.html: displays only if user is logistics officer; displays form to dispose of asset; disposal 
information sent to /dispose_asset; provides links to dashboard and logout
  -already_disposed.html: takes asset tag as 'asset', displays if asset being disposed of was already disposed 
of(based on database state, not date); provides link back to dispose_asset page
  -no_asset.html: takes asset tag as 'asset', displays if asset being disposed of does not exist in database; 
provides link back to dispose_asset page
  -g_report_request.html: takes list of facility lists(item[0] as common name, item[1] as facility code) as 'faclist'; 
displays on 'GET' method request to asset_report; only displays form to make report request; POSTs form data to 
/asset_report
  -p_report_request.html: takes list of facility lists(item[0] as common name, item[1] as facility code) as 
'faclist' and list of report responses as 'results'; displays on 'POST' method request to asset_report; displays 
form for report request and table displaying last requested info; POSTs form data to /asset_report
  -logout.html: takes username as 'username', displays goodbye message on session end; provides link to login page



Can be run directly from wsgi (apachectl start and the pages are good to go!)
