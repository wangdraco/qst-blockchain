from app import db
from sqlalchemy import inspect

class channeldevice(db.Model):
    # 表的名字:,或者derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case
    __tablename__ = 'base_channeldevice'
    #colums
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, unique=False, nullable=True)
    channelunit_id = db.Column(db.Integer, unique=False, nullable=True)
    device_name = db.Column(db.String(80), unique=False, nullable=False)
    startfrom = db.Column(db.Integer, unique=False, nullable=True)
    quantity = db.Column(db.Integer, unique=False, nullable=True)
    data_type = db.Column(db.String(80), unique=False, nullable=True)
    alert_operate = db.Column(db.String(5), unique=False, nullable=True)
    alert_value = db.Column(db.String(20), unique=False, nullable=True)
    component_id = db.Column(db.String(80), unique=False, nullable=True)
    ispushmessage = db.Column(db.String(6), unique=False, nullable=True)
    pushchannelname = db.Column(db.String(6), unique=False, nullable=True)
    iswritedb =db.Column(db.String(6), unique=False, nullable=True)
    status = db.Column(db.String(5), unique=False, nullable=True)
    client_id = db.Column(db.Integer, unique=False, nullable=True)
    isactive = db.Column(db.String(5), unique=False, nullable=True)
    istransfer = db.Column(db.String(6), unique=False, nullable=True)
    offset = db.Column(db.Float, unique=False, nullable=True)
    original_min = db.Column(db.Float, unique=False, nullable=True)
    original_max = db.Column(db.Float, unique=False, nullable=True)
    eng_min = db.Column(db.Float, unique=False, nullable=True)
    eng_max = db.Column(db.Float, unique=False, nullable=True)
    final_result = db.Column(db.String(20), unique=False, nullable=True)
    original_result = db.Column(db.String(20), unique=False, nullable=True)
    data_order = db.Column(db.String(80), unique=False, nullable=True)

    def __repr__(self):
       return f'<{self.device_name},start={self.startfrom},quantity={self.quantity},' \
              f'original={self.original_result},final={self.final_result}>---'

    def toDict(self):#要想使用json.dump(model)进行序列化，必须有这个方法，然后调用json.dump(model.toDict())
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}








