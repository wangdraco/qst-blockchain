# coding: utf-8


from app import db


class SysOrg(db.Model):
    __tablename__ = 'sys_org'

    id = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String(56))
    DESCRIPTION = db.Column(db.String(512))
    ADDRESS = db.Column(db.String(560))
    PHONE = db.Column(db.String(56))
    MOBILE = db.Column(db.String(56))
    FAX = db.Column(db.String(56))
    CONTACT = db.Column(db.String(56))
    ISACTIVE = db.Column(db.String(10))
    ORG_PID = db.Column(db.Integer)
    ORG_CODE = db.Column(db.String(50))
    CREATED = db.Column(db.DateTime)
    CREATEBY = db.Column(db.Integer)
    UPDATED = db.Column(db.DateTime)
    UPDATEBY = db.Column(db.Integer)
    CLIENT_ID = db.Column(db.ForeignKey('sys_client.id'), nullable=False, index=True)
    REMOVE = db.Column(db.String(1))
    ambegin = db.Column(db.DateTime)
    amend = db.Column(db.DateTime)
    pmbegin = db.Column(db.DateTime)
    pmend = db.Column(db.DateTime)
    satisno = db.Column(db.String(45))
    sunisno = db.Column(db.String(45))

    sys_client = db.relationship('SysClient', primaryjoin='SysOrg.CLIENT_ID == SysClient.id', backref='sys_orgs')
