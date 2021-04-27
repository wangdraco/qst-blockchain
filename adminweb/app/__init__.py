from flask import Flask,session,request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_socketio import SocketIO
from .process_logs import log_class
from .process_celery import make_celery,MyTask,CallbackTask
import pickle,threading

app = Flask(__name__)

# login management
login = LoginManager(app)

# import !!  Configurations,access the  config.py
app.config.from_object('config')
app.config['DEBUG'] = False
#create the SQLAlchemy object by passing it the application.
db = SQLAlchemy(app)

#config global connected 4G client socket
client_socket = {}
#use redis as socketio MQ
try:
    from redis import Redis
    r = Redis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"])
    r.ping()
    socketio = SocketIO(app, message_queue='redis://{}:{}'.format(app.config["REDIS_HOST"], app.config["REDIS_PORT"]),
                        manage_session=False)
    print('redis starting...............',r)
except Exception as e:
    print(e)
    socketio = SocketIO(app, async_mode='eventlet',ping_interval=20)

#也可以从外部进程发出event，例如从Celery worker内发出，可以使用下面的方式
#这种方式中，app实例就不需要传递给socketIO了
# socketio = SocketIO(message_queue='redis://')
# socketio.emit('my event', {'data': 'foo'}, namespace='/test')

#use flask-session and redis,在redis中存储session，需要在config中配置session选项
Session(app)

#use Celery as task queue!!
#celery = make_celery(app)
# celery.conf.update(
#     CELERY_ACCEPT_CONTENT = ['json'],
#     CELERY_TASK_SERIALIZER = 'json',
#     CELERY_RESULT_SERIALIZER = 'json',
# )

#log to files
# log = log_class(app, app.config['DEBUG'], 'logs', 'app.logs', 10240, 200)

#启动一些定时任务
# from app.mod_protocalchannel.modbus_tcp_task import schedule_tcpip_task
# t = threading.Thread(target=schedule_tcpip_task)
# t.start()

from app.mod_protocalchannel.modbus_gprs_task import schedule_gprs_task
t = threading.Thread(target=schedule_gprs_task)
t.start()

# from app.mod_protocalchannel.modbus_gprs_task import run_protocal_socket
# tt = threading.Thread(target=run_protocal_socket)
# tt.start()

print('begin in app.__init__ ===============================')



@app.route('/set/')
def set():
    print('==',request)
    _list = [1,2,3]
    # An arbitrary collection of objects supported by pickle.
    data = {
        'a': [1, 2.0, 3, 4 + 6j]*100,
        'b': ("character string", b"byte string"),
        'c': {None, True, False}
    }
    # log.info(str(data))

    session['s-key'] = pickle.dumps(data, pickle.HIGHEST_PROTOCOL )
    return 'ok'

@app.route('/get/')
def get():
    print(pickle.loads(session.get('s-key', 'not set')))
    return str(pickle.loads(session.get('s-key', 'not set')))

@app.route('/test')
def test():
    # 返回元组时，顺序依次是：返回内容，返回状态码，返回的header
    return 'hello world', 200, {'Location':'www.baidu.com'}


#page navigation,所有有导航的模块,都必须在这里引入一下,否则没法注册app.route()
from app  import views, process_fileupload
from app.mod_user import forms
from app.mod_nbiot import forms
from app.mod_loragate import forms
from app.mod_client import forms
from app.mod_org import forms
from app.mod_role import forms
from app.mod_light import forms
from app.mod_modbus import modbus_request
from app.mod_protocalchannel import forms


