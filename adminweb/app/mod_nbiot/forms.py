# coding: utf-8
from app import app
from flask_login import login_required
from flask import render_template,request,redirect,flash,session
import app.mod_nbiot.service as c
from app.mod_nbiot.models import BaseNbiotdevice
import datetime


#导航页面里的href上使用 <a class="" href="{{ url_for('list_all_nbiotdevice') }}"> 或  href="/nbiotdevice/list"都可以路由到这里
@app.route('/nbiotdevice/list')
@login_required
def list_all_nbiotdevice():
    _listdata = c.get_all_data()
    return render_template("nbiot/nbiotdevicelist.html",listdata= _listdata)


@app.route('/nbiotdevice/edit/<int:id>')
@login_required
def edit_nbiotdevice(id):
    selectdata = BaseNbiotdevice()
    if (id != 0):
        selectdata = c.select_by_id(id)
    else:
        selectdata.id = 0
    return render_template("nbiot/nbiotdeviceform.html",selectdata= selectdata)

@app.route('/nbiotdevice/save',methods=['POST'])
def save_nbiotdevice():
    record = BaseNbiotdevice()
    record.id = int(request.form.get('record_id'))

    #better using dict.get() than form[key] ,coz get(key) returns None if no key found.....
    #or use request.form.get('abc','default value').
    record.device_name = request.form.get('device_name')

    record.device_no = request.form.get('device_no')
    record.protocal_type = request.form.get('protocal_type')
    record.server_ip = request.form.get('server_ip')
    record.server_port = request.form.get('server_port')
    record.comment = request.form.get('comment')

    c.update_insert_data(record)
    flash('用户保存成功!!', 'save_info')

    #listdata = c.get_all_data()
    #return render_template("nbiot/nbiotdevicelist.html", listdata=listdata)
    return redirect('/nbiotdevice/list')

@app.route('/nbiotdevice/delete/<int:id>')
@login_required
def delete_nbiotdevice(id):
    c.delete_by_id(id)
    flash('信息删除成功!!', 'delete_info')
    return redirect('/nbiotdevice/list')
