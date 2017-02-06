#Adapted from preflight in dellswor/lost
#Prepare database:

cd sql
psql $1 -f create_tables.sql


#Bring in data and load into database
bash ./import_data.sh $1 5432 #my import_data pulls in legacy data as well
rm -rf osnap_legacy osnap_legacy.tar.gz
cd ..

#Install wsgi files:
cp -R src/* $HOME/wsgi
