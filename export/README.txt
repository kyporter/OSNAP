export_data.sh: takes database name to be exported from and directory name where 
files should be exported to **DELETES ALL FILES CURRENTLY IN DIRECTORY**; runs 
python scripts which will export data to files users.csv, facilities.csv, assets.csv and transfers.csv in target directory

export_data_safe.sh: same as export_data.sh, except doesn't delete files, just 
overwrites target .csv files if they already exist

export_data.py: python script that does most of the work: takes database name and 
directory; writes data to users.csv, facilities.csv, assets.csv, and 
transfers.csv; **Note: stores Null values as 'NULL' string**
