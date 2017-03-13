DB_NAME=$1
DIR_NAME=$2

mkdir -p $2

python export_data.py $DB_NAME $DIR_NAME
