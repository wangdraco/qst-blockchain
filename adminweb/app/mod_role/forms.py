# coding: utf-8
from app import app
from flask_login import login_required
from flask import render_template,request,redirect,flash,session
import app.mod_role.service as c
from app.mod_role.models import SysRole
import datetime,copy


#导航页面里的href上使用 <a class="" href="{{ url_for('list_all_role') }}"> 或  href="/role/list"都可以路由到这里
@app.route('/role/list')
@login_required
def list_all_role():
    _listdata = c.get_all_data()
    return render_template("role/rolelist.html",listdata= _listdata)


@app.route('/role/edit/<int:id>')
@login_required
def edit_role(id):
    selectdata = SysRole()
    if (id != 0):
        selectdata = c.select_by_id(id)
    else:
        selectdata.id = 0
    return render_template("role/roleform.html",selectdata= selectdata)

@app.route('/role/save',methods=['POST'])
@login_required
def save_role():
    record = SysRole()
    record.id = int(request.form.get('record_id'))

    #better using dict.get() than form[key] ,coz get(key) returns None if no key found.....
    #or use request.form.get('abc','default value').
    record.RoleName = request.form.get('RoleName')

    record.Description = request.form.get('Description')
    record.ISACTIVE = request.form.get('ISACTIVE')


    _selectdata = copy.copy(record)

    _selectdata.id = c.update_insert_data(record)
    flash('用户保存成功!!', 'save_info')

    #listdata = c.get_all_data()
    #return render_template("role/rolelist.html", listdata=listdata)
    #return redirect('/role/list')
    return render_template("/role/roleform.html", selectdata= _selectdata)

@app.route('/role/delete/<int:id>')
@login_required
def delete_role(id):
    c.delete_by_id(id)
    flash('信息删除成功!!', 'delete_info')
    return redirect('/role/list')
