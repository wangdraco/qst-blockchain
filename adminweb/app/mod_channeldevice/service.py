from app.mod_channeldevice.models import channeldevice

def get_all_channeldevices():
    return channeldevice.query.all()

def select_by_id(id):
    return channeldevice.query.filter_by(id=id).first()


def select_by_channelunit_id(_id):
    return channeldevice.query.filter_by(channelunit_id=_id).all()

def select_by_ClientAndIsactive(_clientid,_isactive):
    return channeldevice.query.filter_by(client_id=_clientid,isactive=_isactive).all()

