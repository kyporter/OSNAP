DB_NAME=$1
DIR_NAME=$2

mkdir -p $DIR_NAME

python export_data.py $DB_NAME $DIR_NAME
