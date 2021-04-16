from app import db


class channelunit(db.Model):
    # 表的名字:,或者derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case
    __tablename__ = 'base_channelunit'
    #colums
    id = db.Column(db.Integer, primary_key=True)
    protocalchannel_id = db.Column(db.Integer, unique=False, nullable=True)
    unit_id = db.Column(db.Integer, unique=False, nullable=True)
    device_name = db.Column(db.String(80), unique=False, nullable=False)
    device_type = db.Column(db.String(80), unique=False, nullable=False)
    deviceno = db.Column(db.Integer, unique=False, nullable=True)
    refresh_time = db.Column(db.Integer, unique=False, nullable=True)
    batchread = db.Column(db.String(5), unique=False, nullable=True)
    function_code = db.Column(db.String(20), unique=False, nullable=True)
    startfrom = db.Column(db.Integer, unique=False, nullable=True)
    quantity = db.Column(db.Integer, unique=False, nullable=True)
    status = db.Column(db.String(5), unique=False, nullable=True)
    client_id = db.Column(db.Integer, unique=False, nullable=True)
    isactive = db.Column(db.String(5), unique=False, nullable=True)

    def __repr__(self):
       return '<channelunit %r>' % self.device_name








