# coding: utf-8

from sqlalchemy import text
from app import db

class BaseNbiotdevice(db.Model):
    __tablename__ = 'base_nbiotdevice'

    id = db.Column(db.Integer, primary_key=True)
    card_no = db.Column(db.String(20))
    card_name = db.Column(db.String(255))
    device_no = db.Column(db.String(50))
    device_name = db.Column(db.String(255), default=text('ddd'))
    token = db.Column(db.String(40))
    protocal_type = db.Column(db.String(20))
    local_ip = db.Column(db.String(30))
    local_port = db.Column(db.String(8))
    server_ip = db.Column(db.String(30))
    server_port = db.Column(db.String(8))
    send_time = db.Column(db.Integer)
    write_time = db.Column(db.Integer)
    pub_topic = db.Column(db.String(100))
    sub_topic = db.Column(db.String(100))
    isactive = db.Column(db.String(5))
    status = db.Column(db.String(5))
    created = db.Column(db.DateTime, server_default=db.FetchedValue())
    client_id = db.Column(db.Integer)
    data_format = db.Column(db.String(255))
    comment = db.Column(db.String(255))
