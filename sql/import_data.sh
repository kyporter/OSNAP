curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > osnap_legacy.tar.gz

tar -xvzf osnap_legacy.tar.gz

./populate_tables.sh

rm populate_tables.sh
rm parseforsql.py
rm printresults.sql
