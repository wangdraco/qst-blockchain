from flask import json
import os

jsonconf = json.load(open('temp_config.json',encoding='utf-8'))

#create folder first
if not os.path.exists(jsonconf['class_path'] +jsonconf['relative_path']):
    os.mkdir(jsonconf['class_path'] +jsonconf['relative_path'])
if not os.path.exists(jsonconf['web_path']  + jsonconf['webfile_path']):
    os.mkdir(jsonconf['web_path']  + jsonconf['webfile_path'])

#马上修改models.py文件,注意里面的主键id必须是小写的！
def alter_models():
    file_data = ""
    model_file = jsonconf['class_path'] +jsonconf['relative_path']+'/'+'models.py'
    with open(model_file, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if 'from sqlalchemy' in line or 'from flask_sqlalchemy' in line:
                line = line.replace(line, '')

            if 'db = SQLAlchemy()' in line:
                line = line.replace(line, 'from app import db')

            file_data += line

    with open(model_file,"w",encoding="utf-8") as f:
        f.write(file_data)


#create models.py first, use flask-sqlacodegen (pip install flask-sqlacodegen first)
# 同时把form文件注册到__init__中，from app.mod_xxx import forms
_cmd = 'flask-sqlacodegen --flask --tables '+jsonconf['table_name']+' --outfile '\
       +jsonconf['class_path'] +jsonconf['relative_path']+'/'+'models.py'+\
       ' mysql+mysqlconnector://energy:energy168@127.0.0.1/clouddata'
os.system(_cmd)
#os.system是阻塞的，可以使用os.popen(cmd)

#修改models.py文件,db变量引用自app,
alter_models()

#open template files
with open('forms_temp.txt', 'r',encoding='utf-8') as f:
    forms = f.read()

with open('service_temp.txt', 'r',encoding='utf-8') as f:
    service = f.read()

with open('weblist_temp.html', 'r',encoding='utf-8') as f:
    weblist = f.read()

with open('webform_temp.html', 'r',encoding='utf-8') as f:
    webform = f.read()

for k, v in jsonconf.items():
    print(k,v)
    forms = forms.replace('$'+str(k)+'$',str(v))
    service = service.replace('$'+str(k)+'$',str(v))

    weblist = weblist.replace('$'+str(k)+'$',str(v))
    webform = webform.replace('$' + str(k) + '$', str(v))

    if k == 'column_lable' or k == 'column_value':
        for kk,vv in v.items():
            forms = forms.replace('$' + str(kk) + '$', vv)
            weblist = weblist.replace('$' + str(kk) + '$', vv)
            webform = webform.replace('$' + str(kk) + '$', vv)



#生成 forms.py
with open(jsonconf['class_path'] +jsonconf['relative_path']+ '/' +'forms.py','x',encoding='utf-8') as f:
    f.write(forms)

#生成 service.py
with open(jsonconf['class_path'] + jsonconf['relative_path'] + '/' + 'service.py','x',encoding='utf-8') as f:
    f.write(service)

#生成 weblist 文件
with open(jsonconf['web_path']  + jsonconf['webfile_path'] + '/' + jsonconf['list_webfile'], 'x',encoding='utf-8') as f:
    f.write(weblist)

#生成 webform 文件
with open(jsonconf['web_path']  + jsonconf['webfile_path'] + '/' + jsonconf['form_webfile'], 'x',encoding='utf-8') as f:
    f.write(webform)

print('生成成功-----------------------------------')