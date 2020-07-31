# coding: utf-8
from app.mod_nbiot.models import BaseNbiotdevice
from app import db

def get_all_data():
    return BaseNbiotdevice.query.all()

def select_by_id(id):
    return BaseNbiotdevice.query.filter_by(id=id).first()

def delete_by_id(id):
    record = BaseNbiotdevice.query.filter_by(id=id).first()
    db.session.delete(record)
    db.session.commit()

#update or insert data
def update_insert_data(data):
    if (data.id == 0):
        db.session.add(data)
        db.session.commit()
    else:
        _data = data.__dict__
        #update接受的参数是个字典，里面有要更新的字段和对应的值，所以要把无用的数据pop掉
        _data.pop('_sa_instance_state')
        BaseNbiotdevice.query.filter_by(id=data.id).update(_data)
        db.session.commit()


