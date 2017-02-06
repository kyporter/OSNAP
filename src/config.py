##code from dellswor/lost, comments are me figuring out what each line is doing and documenting it for future me

import json

import os
import pathlib

cpath = pathlib.Path(os.path.realpath(__file__)).parent.joinpath('lost_config.json') ##finding path so that the config 
##can be open wherever it is

with cpath.open() as conf:    ##opening config file
    c = json.load(conf)		##importing configuration 'dictionary'
    dbname = c['database']['dbname']
    dbhost = c['database']['dbhost']
    dbport = c['database']['dbport']
