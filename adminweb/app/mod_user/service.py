from app.mod_user.models import User
from app import db
import hashlib,copy
def get_all_data():
    return User.query.all()

def select_by_id(id):
    return User.query.filter_by(id=id).first()

#update or insert data
def update_insert_data(data):
    _id = data.id
    if (_id == 0):
        # _data = User()
        # print('data.__dict__',data.__dict__)
        # for k, v in data.__dict__.items():
        #     if k not in ('_sa_instance_state','id'):
        #         setattr(_data, k, v)
        #important!!!, coz id is autoincrecement,so delete it from properties,or it will not return inserted ID
        delattr(data, "id")
        print('after delte ,data is ',data.__dict__)

        db.session.add(data)
        db.session.commit()

        #get inserted ID
        _id = data.id
    else:
        #data = {'username': user.username, 'real_name': user.real_name, 'created': user.created}
        _data = data.__dict__
        # update接受的参数是个字典，里面有要更新的字段和对应的值，所以要把无用的数据pop掉
        _data.pop('_sa_instance_state')
        User.query.filter_by(id=data.id).update(_data)
        db.session.commit()
    print('final id is ===============,',_id)
    return _id


def select_by_name(name):
    return User.query.filter_by(username=name).first()

def select_by_password(name,password):
    return User.query.filter_by(username=name,password=md5(password)).first()

def delete_by_id(id):
    record = User.query.filter_by(id=id).first()
    db.session.delete(record)
    db.session.commit()

def md5(_password):
    _p = hashlib.md5()
    _p.update(bytes(_password,encoding='utf-8'))
    return _p.hexdigest()