# coding: utf-8


from app import db

class SysRole(db.Model):
    __tablename__ = 'sys_role'

    id = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.String(20), nullable=False)
    Description = db.Column(db.String(100))
    CREATED = db.Column(db.DateTime)
    CREATEBY = db.Column(db.Integer)
    UPDATED = db.Column(db.DateTime)
    UPDATEBY = db.Column(db.Integer)
    REMOVE = db.Column(db.String(1))
    ISACTIVE = db.Column(db.String(10))
    CLIENT_ID = db.Column(db.Integer, nullable=False)
