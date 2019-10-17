# Import flask and template operators
from flask import Flask, json,session,render_template,make_response,jsonify
from flask_login import LoginManager,current_user,login_required
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import memcache,socket
import eventlet,sys
from flask_httpauth import HTTPTokenAuth
import threading
from datetime import timedelta
import concurrent.futures

#sys.setrecursionlimit(30000)
# Define the WSGI application object
app = Flask(__name__)
#默认缓存控制的最大期限,用于static目录的更新通知,默认12小时
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=5)

#有了这个patch,debug就不起作用了
eventlet.monkey_patch()
socketio = SocketIO(app, async_mode='eventlet',ping_interval=20)
#web socket instance,mode='eventlet''threading
# async_mode='eventlet'导致页面没反应
#加上eventlet.monkey_patch()就可以了,但是eventlet不适用于多个socketio的情况，在多线程里不能使用多个socketio对象
#socketio = SocketIO(app, async_mode='threading')

# import !!  Configurations,access the  config.py
app.config.from_object('config')

#create the SQLAlchemy object by passing it the application.
db = SQLAlchemy(app)

# login management
login = LoginManager(app)


# Json config
#jsonconf = json.load(open(app.config['JSON_CONFIG_PATH']))

#config global connected client socket
client_socket = {}


@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.id


@login.unauthorized_handler
def unauthorized_handler():
    #return 'Unauthorized'
    return render_template("session_timeout.html")



#start memcached
mc = memcache.Client(['127.0.0.1:11211'], debug=True)


#避免eventlet冲突,每次都要生成一个新的memcache
def get_memcache():
    return memcache.Client(['127.0.0.1:11211'], debug=True)



#start therad for receiving HR data at 5001 port
from app.mod_socket.TcpServer import run_tcpserver
_server = threading.Thread(target=run_tcpserver)
#_server.start()



#中铁华润项目，自动喷淋
from app.mod_zthr.process_autodust import run_scheduled_task
autodust_t = threading.Thread(target=run_scheduled_task)
#autodust_t.start()

#中铁建工信联天地项目-青岛, 环境监测数据
from app.mod_xltd.process_dust import run_dust_scheduled_task
t_dust_data = threading.Thread(target=run_dust_scheduled_task, kwargs={'mc_instance': mc})
t_dust_data.start()

#中铁建工信联天地项目-青岛, 塔吊监测数据
# from app.mod_xltd.process_tower import run_tower_scheduled_task
# t_tower_data = threading.Thread(target=run_tower_scheduled_task, kwargs=None)
# t_tower_data.start()
#run_tower_data()
#executor=concurrent.futures.ThreadPoolExecutor(max_workers=3)
#executor.map(run_tower_data)


#中铁建工信联天地项目-青岛, 养护室温湿度数据
from app.mod_xltd.process_yanghushi import run_yanghushi_scheduled_task
t_yanghushi_data = threading.Thread(target=run_yanghushi_scheduled_task, kwargs={'mc_instance': mc})
#t_yanghushi_data.start()

#中铁建工信联天地项目-青岛, 电表数据
from app.mod_xltd.process_electronic import run_scheduled_task
t_elec_data = threading.Thread(target=run_scheduled_task, kwargs={'mc_instance': mc})
t_elec_data.start()


#manualy gc.collect,realease memory
# from app.mod_tools.gc_thread import run_gc_thread
# gc_t = threading.Thread(target=run_gc_thread)
# gc_t.start()

#check base_connectinfo table ,if timeout >1 hour,then send message
#from app.mod_connectinfo.controllers import check_msgtime
#msg = threading.Thread(target=check_msgtime)
#msg.start()

#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#serializer = Serializer(app.config['SECRET_KEY'], expires_in=1800) # 1800 seconds
from itsdangerous import JSONWebSignatureSerializer as Serializer
serializer = Serializer(app.config['SECRET_KEY'])

users = ['John', 'Susan']
for user in users:
    token = serializer.dumps({'username': user})
    print('Token for {}: {}\n'.format(user, token))


#api token authentication
auth = HTTPTokenAuth(scheme='Bearer')

# tokens = {
#     "secret-token-1": "John",
#     "secret-token-2": "Susan"
# }
@auth.verify_token
def verify_token(token):

    # if token in tokens:
    #     print('----------------------',tokens[token])
    #     return True
    # return False
    try:
        data = serializer.loads(token)
        print('the loads data is ================',data)
    except:
        return False
    if 'username' in data:
        print('Authentication is succeed !!!!!!!', data['username'])
        return True
    return False

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)



#page navigation,所有有导航的模块,都必须在这里引入一下,否则没法注册app.route()
from app  import views
from app.mod_xltd import process_websocket
