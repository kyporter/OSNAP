create_tables.sql : SQL script to create datamodel-related tables for the LOST database

parseforsql.py : python script that goes through each (relevant) legacy file and puts the information into SQL instructions

import_data.sh : Shell script that: 1. imports legacy data with curl and unzips it; 2. updates port information per port variable; 
3. executes parseforsql.py and writes its results to printresults.sql; 4. executes printresults.sql in the variable-specified database; 
5. removes printresults.sql
