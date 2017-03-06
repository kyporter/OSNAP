create_tables.sql : SQL script to create datamodel-related tables for the LOST database; 
currently creates:
 table 'users' which stores unique username, password, and 
active/inactive status, indexed by user_pk, also stores role_fk
 table 'roles' which stores roles by title and description
 table 'assets' which stores assets by tag and description
 table 'facilities' which stores facilities by common name and <=6 char code
 table 'asset_history' which stores asset current and past locations, with 
departure and arrival dates
 table 'transfer_requests' which stores all information relevant to making, 
approving, and tracking a transfer request
 Populates roles table, stores 'in transit' entry in facilities
