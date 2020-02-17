from flask import Flask

app = Flask(__name__)

# import !!  Configurations,access the  config.py
app.config.from_object('config')



#page navigation,所有有导航的模块,都必须在这里引入一下,否则没法注册app.route()
from app  import views