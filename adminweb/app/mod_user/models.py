from app import db
from flask_login import UserMixin
import datetime
from sqlalchemy import func
#继承UserMixin,使用户模块支持登录功能
class User(db.Model,UserMixin):
    # 表的名字:,或者derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case
    __tablename__ = 'sys_user'
    #colums
    id = db.Column(db.Integer,autoincrement=True,  primary_key=True)
    ORG_ID = db.Column(db.Integer,default=0)
    CLIENT_ID = db.Column(db.Integer, default=0)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    real_name = db.Column(db.String(80), unique=True, nullable=True)
    isactive = db.Column(db.String(20),  nullable=True)
    theme = db.Column(db.String(80), default='theme', nullable=True)
    email = db.Column(db.String(80), nullable=True)
    created = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, onupdate=datetime.datetime.now, nullable=True)
    defaultpage = db.Column(db.String(80), nullable=True)
    logoimage = db.Column(db.String(80), nullable=True)

    def __init__(self, username='', password='', real_name='', isactive='', theme='',
                 email='', created=datetime.date.today(),defaultpage=''):
        #self.id = id
        self.username = username
        self.password = password
        self.real_name = real_name
        self.isactive = isactive
        self.theme = theme
        self.email = email
        self.created = created
        self.defaultpage = defaultpage

    # def __repr__(self):
    #     return f'User<id={self.id},username={self.username},realname= {self.real_name}>'








