# coding: utf-8
from app import app
from flask_login import login_required
from flask import render_template,request,redirect,flash,session
import app.mod_client.service as c
from app.mod_client.models import SysClient
import datetime,copy


#导航页面里的href上使用 <a class="" href="{{ url_for('list_all_client') }}"> 或  href="/client/list"都可以路由到这里
@app.route('/client/list')
@login_required
def list_all_client():
    _listdata = c.get_all_data()
    return render_template("client/clientlist.html",listdata= _listdata)


@app.route('/client/edit/<int:id>')
@login_required
def edit_client(id):
    selectdata = SysClient()
    if (id != 0):
        selectdata = c.select_by_id(id)
    else:
        selectdata.id = 0
    return render_template("client/clientform.html",selectdata= selectdata)

@app.route('/client/save',methods=['POST'])
@login_required
def save_client():
    record = SysClient()
    record.id = int(request.form.get('record_id'))

    #better using dict.get() than form[key] ,coz get(key) returns None if no key found.....
    #or use request.form.get('abc','default value').
    record.NAME = request.form.get('NAME')

    record.CLIENTADDRESS = request.form.get('CLIENTADDRESS')
    record.POP_SERVER = request.form.get('POP_SERVER')
    record.SMTP_SERVER = request.form.get('SMTP_SERVER')
    record.ISACTIVE = request.form.get('ISACTIVE')
    record.DESCRIPTION = request.form.get('DESCRIPTION')

    _selectdata = copy.copy(record)

    _selectdata.id = c.update_insert_data(record)
    flash('用户保存成功!!', 'save_info')

    #listdata = c.get_all_data()
    #return render_template("client/clientlist.html", listdata=listdata)
    #return redirect('/client/list')
    return render_template("/client/clientform.html", selectdata= _selectdata)

@app.route('/client/delete/<int:id>')
@login_required
def delete_client(id):
    c.delete_by_id(id)
    flash('信息删除成功!!', 'delete_info')
    return redirect('/client/list')
