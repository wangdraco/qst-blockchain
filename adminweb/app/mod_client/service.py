# coding: utf-8
from app.mod_client.models import SysClient
from app import db

def get_all_data():
    return SysClient.query.all()

def select_by_id(id):
    return SysClient.query.filter_by(id=id).first()

def delete_by_id(id):
    record = SysClient.query.filter_by(id=id).first()
    db.session.delete(record)
    db.session.commit()

#update or insert data
def update_insert_data(data):
    _id = data.id
    if (_id == 0):
        delattr(data, "id")
        db.session.add(data)
        db.session.commit()
        #get inserted ID
        _id = data.id
    else:
        _data = data.__dict__
        #update接受的参数是个字典，里面有要更新的字段和对应的值，所以要把无用的数据pop掉
        _data.pop('_sa_instance_state')
        SysClient.query.filter_by(id=data.id).update(_data)
        db.session.commit()
    return _id


