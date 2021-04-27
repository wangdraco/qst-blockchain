from app import db
from app.mod_protocal.models import BaseProtocal

class protocalchannel(db.Model):
    # 表的名字:,或者derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case
    __tablename__ = 'base_protocalchannel'
    #colums
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(80), unique=True, nullable=False)
    protocal_id = db.Column(db.ForeignKey('base_protocal.id'), unique=False, nullable=True)
    time_out = db.Column(db.Integer, unique=False, nullable=True)
    refreshtime = db.Column(db.Integer, unique=False, nullable=True)
    port = db.Column(db.String(20), unique=False, nullable=True)
    ipaddress = db.Column(db.String(80), unique=False, nullable=True)
    baudrate = db.Column(db.Integer, unique=False, nullable=True)
    databit = db.Column(db.Integer, unique=False, nullable=True)
    stopbit = db.Column(db.Integer, unique=False, nullable=True)
    parity = db.Column(db.String(6), unique=False, nullable=True)
    status = db.Column(db.String(5), unique=False, nullable=True)
    client_id = db.Column(db.Integer, unique=False, nullable=True)
    created = db.Column(db.DateTime, nullable=False)
    connettype = db.Column(db.String(20), unique=False, nullable=True)
    comment = db.Column(db.String(80), unique=False, nullable=True)
    isactive = db.Column(db.String(5), unique=False, nullable=True)
    realtime = db.Column(db.String(5), unique=False, nullable=True)

    protocal = db.relationship('BaseProtocal', primaryjoin='protocalchannel.protocal_id == BaseProtocal.id')


    def __repr__(self):
        return f'<protocalchannel: {self.channel_name}>'








