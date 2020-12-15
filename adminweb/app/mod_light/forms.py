# coding: utf-8
from app import app
from flask_login import login_required
from flask import render_template,request,redirect,flash,session
import app.mod_light.service as c
from app.mod_light.models import BaseLight
import datetime,copy,time
from pymodbus.client.sync import ModbusTcpClient


#导航页面里的href上使用 <a class="" href="{{ url_for('list_all_light') }}"> 或  href="/light/list"都可以路由到这里
@app.route('/light/list')
@login_required
def list_all_light():
    _listdata = c.get_all_data()
    _listdata = operate_status(_listdata)

    return render_template("light/lightlist.html",listdata= _listdata)


@app.route('/light/edit/<int:id>')
@login_required
def edit_light(id):
    selectdata = BaseLight()
    if (id != 0):
        selectdata = c.select_by_id(id)
    else:
        selectdata.id = 0
    return render_template("light/lightform.html",selectdata= selectdata)

@app.route('/light/save',methods=['POST'])
@login_required
def save_light():
    record = BaseLight()
    record.id = int(request.form.get('record_id'))

    #better using dict.get() than form[key] ,coz get(key) returns None if no key found.....
    #or use request.form.get('abc','default value').
    record.light_name = request.form.get('light_name')

    record.position = request.form.get('position')
    record.gateway_channel = request.form.get('gateway_channel')
    record.ip_address = request.form.get('ip_address')
    record.ip_port = request.form.get('ip_port')
    record.unit_id = request.form.get('unit_id')
    record.reg_address = request.form.get('reg_address')
    record.reg_length = request.form.get('reg_length')

    _selectdata = copy.copy(record)

    _selectdata.id = c.update_insert_data(record)
    flash('数据保存成功!!', 'save_info')

    #listdata = c.get_all_data()
    #return render_template("light/lightlist.html", listdata=listdata)
    #return redirect('/light/list')
    return render_template("/light/lightform.html", selectdata= _selectdata)

@app.route('/light/delete/<int:id>')
@login_required
def delete_light(id):
    c.delete_by_id(id)
    flash('信息删除成功!!', 'delete_info')
    return redirect('/light/list')


def operate_status(_list):
    #client = ModbusTcpClient('192.168.7.151', port=6002)
    #result = client.read_holding_registers(3, 12, unit=9, signed=True)

    l = []
    for d in _list:
        try:
            client = ModbusTcpClient(d.ip_address, port=d.ip_port)
            result = client.read_holding_registers(d.reg_address, d.reg_length, unit=d.unit_id, signed=True)
            d.status = result.registers[0]

        except:
            d.status = 2
            print('error ')
        l.append(d)
        time.sleep(0.03)

    client.close()
    return l


@app.route('/powerbox/list')
@login_required
def list_all_powerbox():
    _listdata = []
    d1 = {"power_name":"1AA隔离开关","position":"综合楼1层","ip_address":"192.168.7.241","status":"开"}
    d2 = {"power_name": "3AA有源滤波柜", "position": "综合楼1层", "ip_address": "192.168.7.241", "status": "开"}
    d3 = {"power_name": "4AA出线柜", "position": "2#楼", "ip_address": "192.168.7.241", "status": "关"}
    d4 = {"power_name": "5AA出线柜", "position": "2#楼", "ip_address": "192.168.7.241", "status": "关"}
    d5 = {"power_name": "6AA出线柜", "position": "3#楼", "ip_address": "192.168.7.241", "status": "开"}
    d6 = {"power_name": "7AA出线柜", "position": "3#楼", "ip_address": "192.168.7.240", "status": "关"}
    d7 = {"power_name": "8AA出线柜", "position": "4#楼", "ip_address": "192.168.7.240", "status": "开"}
    d8 = {"power_name": "9AA出线柜", "position": "5#楼", "ip_address": "192.168.7.240", "status": "开"}
    d9 = {"power_name": "10AA出线柜", "position": "5#楼", "ip_address": "192.168.7.240", "status": "开"}
    _listdata.append(d1)
    _listdata.append(d2)
    _listdata.append(d3)
    _listdata.append(d4)
    _listdata.append(d5)
    _listdata.append(d6)
    _listdata.append(d7)
    _listdata.append(d8)
    _listdata.append(d9)


    return render_template("light/powerboxlist.html",listdata= _listdata)