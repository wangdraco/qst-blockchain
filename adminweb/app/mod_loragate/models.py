# coding: utf-8


from app import db

class BaseLoragate(db.Model):
    __tablename__ = 'base_loragate'

    id = db.Column(db.Integer, primary_key=True)
    gate_no = db.Column(db.String(20))
    gate_name = db.Column(db.String(255))
    gate_addr = db.Column(db.Integer)
    local_ip = db.Column(db.String(30))
    local_port = db.Column(db.Integer)
    server_ip = db.Column(db.String(30))
    server_port = db.Column(db.Integer)
    delay_time = db.Column(db.Integer)
    isactive = db.Column(db.String(5))
    status = db.Column(db.String(5))
    client_id = db.Column(db.Integer)
    comment = db.Column(db.String(255))
    created = db.Column(db.DateTime)
