# coding: utf-8
from app import app
from flask_login import login_required
from flask import render_template,request,redirect,flash,session
import app.mod_org.service as c
from app.mod_org.models import SysOrg
import datetime,copy


#导航页面里的href上使用 <a class="" href="{{ url_for('list_all_org') }}"> 或  href="/org/list"都可以路由到这里
@app.route('/org/list')
@login_required
def list_all_org():
    _listdata = c.get_all_data()
    return render_template("org/orglist.html",listdata= _listdata)


@app.route('/org/edit/<int:id>')
@login_required
def edit_org(id):
    selectdata = SysOrg()
    if (id != 0):
        selectdata = c.select_by_id(id)
    else:
        selectdata.id = 0
    return render_template("org/orgform.html",selectdata= selectdata)

@app.route('/org/save',methods=['POST'])
@login_required
def save_org():
    record = SysOrg()
    record.id = int(request.form.get('record_id'))

    #better using dict.get() than form[key] ,coz get(key) returns None if no key found.....
    #or use request.form.get('abc','default value').
    record.NAME = request.form.get('NAME')

    record.ADDRESS = request.form.get('ADDRESS')
    record.PHONE = request.form.get('PHONE')
    record.FAX = request.form.get('FAX')
    record.ISACTIVE = request.form.get('ISACTIVE')
    record.DESCRIPTION = request.form.get('DESCRIPTION')

    _selectdata = copy.copy(record)

    _selectdata.id = c.update_insert_data(record)
    flash('用户保存成功!!', 'save_info')

    #listdata = c.get_all_data()
    #return render_template("org/orglist.html", listdata=listdata)
    #return redirect('/org/list')
    return render_template("/org/orgform.html", selectdata= _selectdata)

@app.route('/org/delete/<int:id>')
@login_required
def delete_org(id):
    c.delete_by_id(id)
    flash('信息删除成功!!', 'delete_info')
    return redirect('/org/list')
