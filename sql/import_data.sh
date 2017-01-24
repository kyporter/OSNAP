curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > osnap_legacy.tar.gz

tar -xvzf osnap_legacy.tar.gz

postgres -p $1

python parseforsql.py > printresults.sql

psql $2 -f printresults.sql

rm printresults.sql
