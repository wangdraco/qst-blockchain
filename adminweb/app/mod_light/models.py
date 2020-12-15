# coding: utf-8


from app import db

class BaseLight(db.Model):
    __tablename__ = 'base_light_data'

    id = db.Column(db.Integer, primary_key=True)
    light_name = db.Column(db.String(45))
    position = db.Column(db.String(145))
    gateway_channel = db.Column(db.String(45))
    ip_address = db.Column(db.String(45))
    func_code = db.Column(db.String(45))
    ip_port = db.Column(db.Integer)
    unit_id = db.Column(db.Integer)
    reg_address = db.Column(db.Integer)
    reg_length = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    status = db.Column(db.String(45))
    comment = db.Column(db.String(45))
