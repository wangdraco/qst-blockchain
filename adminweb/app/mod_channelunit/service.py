from app.mod_channelunit.models import channelunit

def get_all_channelunits():
    return channelunit.query.all()

def select_by_id(id):
    return channelunit.query.filter_by(id=id).first()


def select_by_protocalchannel_id(_id):
    return channelunit.query.filter_by(protocalchannel_id=_id).all()

def select_by_ClientAndIsactive(_clientid,_isactive):
    return channelunit.query.filter_by(client_id=_clientid,isactive=_isactive).all()

