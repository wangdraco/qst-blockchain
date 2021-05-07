from app.mod_protocal.models import BaseProtocal


def get_all_protocals():
    return BaseProtocal.query.all()

def select_by_id(id):
    return BaseProtocal.query.filter_by(id=id).first()

#filter_by可以不用表名，但只能进行等值查询， 如果要用like，大于，in等查询还得使用filter
def select_by_ids(_ids):
    return BaseProtocal.query.filter(BaseProtocal.id.in_(_ids)).all()


def select_by_status(_status):
    return BaseProtocal.query.filter_by(status=_status).all()





