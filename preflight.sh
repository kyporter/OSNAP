#Adapted from preflight in dellswor/lost
#Prepare database:

cd sql
psql $1 -f create_tables.sql

#Install wsgi files:
cp -R src/* $HOME/wsgi
