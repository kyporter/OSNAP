Contains clients for creating, activating and revoking a user.  
activate_user.py: called with arguments URL username password role; role can be 
logofc or facofc. Information is sent to the update_user route of app.py
revoke_user.py: called with arguments URL username; information is sent to the 
update_user route of app.py
