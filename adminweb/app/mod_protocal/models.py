from app import db


class BaseProtocal(db.Model):
    # 表的名字:,或者derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case
    __tablename__ = 'base_protocal'
    #colums
    id = db.Column(db.Integer, primary_key=True)
    protocal_name = db.Column(db.String(80), unique=False, nullable=True)
    protocal_type = db.Column(db.String(80), unique=False, nullable=True)
    status = db.Column(db.String(5), unique=False, nullable=True)
    client_id = db.Column(db.Integer, unique=False, nullable=True)
    comment = db.Column(db.String(100), unique=False, nullable=True)

    def __repr__(self):
       return '<base_protocal %r>' % self.protocal_name








