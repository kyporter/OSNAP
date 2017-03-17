#! /usr/bin/bash

DB_NAME=$1
DIR_NAME=$2

rm -rf $DIR_NAME
mkdir $DIR_NAME

python export_data.py $DB_NAME $DIR_NAME
