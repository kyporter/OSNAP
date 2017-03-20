  contains .html to give pages content
  -FO_only.html: displays if non-facilities officers try to access transfer 
approval page; provides links to dashboard and logout
  -LO_only.html: displays if non-logistics officers try to access dispose_asset; provides links to dashboard and logout
  -add_asset.html: takes list of asset lists(item[0] as asset_tag, item[1] as description) as 'assets' and list of 
facility lists(item[0] as common name, item[1] as facility code) as 'faclist', displays list of asset 
tags/descriptions currently in database and the form to add new asset; form info POSTs to /add_asset; provides links 
to dashboard and logout
  -add_ast_fail.html: takes asset tag as 'asset', announces failure to add asset and provides link back to add_asset page
  -add_fac_fail.html: takes facility common name as 'c_name', announces failure to add facility and provides link 
back to add_facility page
  -add_facility.html: takes list of facility lists(item[0] as common name, item[1] as facility code) as 'faclist', 
displays list of facility common names/codes and the form to add new facility; POSTs form information to /add_facility, 
provides links to dashboard and logout
  -already_disposed.html: takes asset tag as 'asset', displays if asset being disposed of was already disposed 
of(based on database state, not date); provides link back to dispose_asset page
  -approve_request.html: displays only if user is facilities officer, takes 
'GET' request for request number; POSTs approval or rejection then redirects to 
dashboard
DEPRECATED  -c_user_fail.html: takes username as 'username', announces failure of user creation and provides link to create user page
DEPRECATED  -c_user_success.html: takes username as 'username', announces success of user creation and provides link to login page
DEPRECATED  -create_user.html: renders create user page, POSTs username, password and role to /create_user
  -dashboard.html: takes username as 'username' and role as 'role', displays logged in user's name and role; provides links 
to add_asset, add_facility, asset_report, transfer_report and logout; if user is a logistics officer, provides links to dispose_asset and transfer_req; 
displays requests in progress-for facilities officers, requests to be approved, for logistics officers, requests to have load/unload times set
  -disposal_form.html: displays only if user is logistics officer; displays form to dispose of asset; disposal 
information sent to /dispose_asset; provides links to dashboard and logout
  -g_report_request.html: takes list of facility lists(item[0] as common name, item[1] as facility code) as 'faclist'; 
displays on 'GET' method request to asset_report; only displays form to make report request; POSTs form data to 
/asset_report
  -g_trans_rep.html: gets date to return in transit report for
  -invalid_request.html: default 'you can't do that' page
  -login.html: the login page, username and password POSTed to /login
  -login_fail.html: announces failure of login and provides link back to login page
  -logout.html: takes username as 'username', displays goodbye message on session end; provides link to login page
  -no_asset.html: takes asset tag as 'asset', displays if asset being disposed of does not exist in database; 
provides link back to dispose_asset page
  -p_report_request.html: takes list of facility lists(item[0] as common name, item[1] as facility code) as 
'faclist' and list of report responses as 'results'; displays on 'POST' method request to asset_report; displays 
form for report request and table displaying last requested info; POSTs form data to /asset_report
  -p_trans_rep.html: displays in transit report and provides form to request a 
report for another date
  -request_made.html: indicates successful transfer request has been made, 
provides link to dashboard
  -transfer_req.html: displays dropdown of assets available for transfer and 
their current locations, and a dropdown of possible facilites to be transferred 
to; successful request displays request_made.html
  -update_request.html: if asset has not had a load date set yet, displays load 
date setter; if asset has had load date set but not had unload date set, 
displays unload date setter


Can be run directly from wsgi (apachectl start and the pages are good to go!)
