# OSNAP
preflight.sh : takes one argument(database name) and gets that database setup with tables, 
downloads legacy data and stores it in the database as appropriate, cleans up temp file,
moves src files(including demo lost.pub key) from OSNAP file to the wsgi directory

install_daemons.sh : installs apache and postgres
