# coding: utf-8
from app import app
from flask_login import login_required
from flask import render_template,request,redirect,flash,session
import app.mod_loragate.service as c
from app.mod_loragate.models import BaseLoragate
import datetime,copy


#导航页面里的href上使用 <a class="" href="{{ url_for('list_all_loragate') }}"> 或  href="/loragate/list"都可以路由到这里
@app.route('/loragate/list')
@login_required
def list_all_loragate():
    _listdata = c.get_all_data()
    return render_template("loragate/loragatelist.html",listdata= _listdata)


@app.route('/loragate/edit/<int:id>')
@login_required
def edit_loragate(id):
    selectdata = BaseLoragate()
    if (id != 0):
        selectdata = c.select_by_id(id)
    else:
        selectdata.id = 0
    return render_template("loragate/loragateform.html",selectdata= selectdata)

@app.route('/loragate/save',methods=['POST'])
@login_required
def save_loragate():
    record = BaseLoragate()
    record.id = int(request.form.get('record_id'))

    #better using dict.get() than form[key] ,coz get(key) returns None if no key found.....
    #or use request.form.get('abc','default value').
    record.gate_no = request.form.get('gate_no')

    record.gate_name = request.form.get('gate_name')
    record.gate_addr = request.form.get('gate_addr')
    record.local_ip = request.form.get('local_ip')
    record.local_port = request.form.get('local_port')
    record.comment = request.form.get('comment')

    _selectdata = copy.copy(record)

    c.update_insert_data(record)
    flash('用户保存成功!!', 'save_info')

    #listdata = c.get_all_data()
    #return render_template("loragate/loragatelist.html", listdata=listdata)
    #return redirect('/loragate/list')
    return render_template("loragate/loragateform.html", selectdata= _selectdata)

@app.route('/loragate/delete/<int:id>')
@login_required
def delete_loragate(id):
    c.delete_by_id(id)
    flash('信息删除成功!!', 'delete_info')
    return redirect('/loragate/list')
