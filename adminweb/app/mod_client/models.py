# coding: utf-8


from app import db

class SysClient(db.Model):
    __tablename__ = 'sys_client'

    id = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(50))
    DESCRIPTION = db.Column(db.String(500))
    POP_SERVER = db.Column(db.String(255))
    SMTP_SERVER = db.Column(db.String(100))
    EMAIL_USER = db.Column(db.String(50))
    EMAIL_PWD = db.Column(db.String(100))
    ISACTIVE = db.Column(db.String(10))
    CLIENTADDRESS = db.Column(db.String(100))
    CREATED = db.Column(db.DateTime)
    CREATEBY = db.Column(db.String(50))
    UPDATED = db.Column(db.DateTime)
    UPDATEBY = db.Column(db.String(50))
    REMOVE = db.Column(db.String(1))
    INIT = db.Column(db.Integer, server_default=db.FetchedValue())
