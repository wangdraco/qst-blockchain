# coding: utf-8
from app import app,r
from flask_login import login_required
from flask import render_template,request,redirect,flash
from app.mod_protocalchannel.service import *
from app.mod_protocalchannel.models import protocalchannel
import json



@app.route('/protocalchannel/list')
@login_required
def list_all_protocaldevice():
    _listdata = get_all_protocalchannels()
    return render_template("protocalchannel/protocalchannellist.html",listdata= _listdata)

@app.route('/protocalchannel/edit/<int:id>')
@login_required
def edit_protocalchannel(id):
    selectdata = protocalchannel()
    if (id != 0):
        selectdata = select_by_id(id)
    else:
        selectdata.id = 0
    return render_template("protocalchannel/protocalchannelform.html",selectdata= selectdata)


@app.route('/redis/<int:channel_id>/<int:channel_unit>')
def get_redis_data(channel_id,channel_unit):
    if r.exists(f'channel:{channel_id}:{channel_unit}'):
        return r.exists(f'channel:{channel_id}:{channel_unit}')
    else:
        result = {}
        result['result'] = False
        return json.dumps(result)