curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > osnap_legacy.tar.gz

tar -xvzf osnap_legacy.tar.gz

python parseforsql.py > printresults.sql

psql $1 -f printresults.sql

rm printresults.sql
