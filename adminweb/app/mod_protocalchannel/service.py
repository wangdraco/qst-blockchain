from app.mod_protocalchannel.models import protocalchannel


def get_all_protocalchannels():
    return protocalchannel.query.all()

def select_by_id(id):
    return protocalchannel.query.filter_by(id=id).first()

#filter_by可以不用表名，但只能进行等值查询， 如果要用like，大于，in等查询还得使用filter
def select_by_ids(_ids):
    return protocalchannel.query.filter(protocalchannel.id.in_(_ids)).all()


def select_by_status(_status):
    return protocalchannel.query.filter_by(status=_status).all()

def select_by_isactive(_isactive):
    return protocalchannel.query.filter_by(isactive=_isactive).all()

def select_by_clientAndIsactive(_clientid,_isactive):
    return protocalchannel.query.filter_by(client_id=_clientid,isactive=_isactive).all()



