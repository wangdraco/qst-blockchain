from flask import json
import os

jsonconf = json.load(open('temp_config.json',encoding='utf-8'))
_cmd = 'flask-sqlacodegen --flask --tables '+jsonconf['table_name']+' --outfile '\
       +jsonconf['class_path'] +jsonconf['relative_path']+'/'+'models55.py'+' mysql+mysqlconnector://energy:energy168@127.0.0.1/clouddata'
os.system(_cmd)
#os.popen('flask-sqlacodegen --help')

