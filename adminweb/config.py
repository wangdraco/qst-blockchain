# Statement for enabling the development environment,
# 引用方式: app.config.from_object('config'), config.py里面的 key必须是大写的,
#很多地方就不用写配置了, 比如debug=True, SECRET_KEY等,系统自动从下面取值
DEBUG = True

# Define the application directory
import os
# from sqlalchemy.pool import  Pool,QueuePool
# from sqlalchemy import create_engine,pool
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#redis host
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
# Define the database - we are working with
# SQLite for this example
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'clouddata.db')
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://energy:adminwqc168@139.129.200.70/clouddata?charset=utf8'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://energy:energy168@127.0.0.1/clouddata?charset=utf8'
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://energy:adminwqc168@139.129.200.70/i-yunwei?charset=utf8'

DATABASE_CONNECT_OPTIONS = {}

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URI,
#     poolclass=QueuePool,
#     pool_size=5,     # default in SQLAlchemy
#     max_overflow=10, # default in SQLAlchemy
#     pool_timeout=6,  # raise an error faster than default
# )

SQLALCHEMY_ENGINE_OPTIONS = {
    #'pool': QueuePool(Pool._creator),
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
    'pool_timeout': 30,
    'max_overflow': 50
}


#如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它
SQLALCHEMY_TRACK_MODIFICATIONS = True

#如果设置成 True，SQLAlchemy 将会记录所有 发到标准输出(stderr)的语句，这对调试很有帮助
SQLALCHEMY_ECHO = False


#mysql connettion ,use Mysql's original connector from Oracle,
#SQLALCHEMY_MYSQL_URI = 'mysql+mysqlconnector://energy:energy168@localhost/clouddata?charset=utf8'

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 4

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "admin168."

# Secret key for signing cookies
SECRET_KEY = "!@#qwer$%^"

#session configuration part
from redis import Redis
try:
    SESSION_TYPE = "redis" #session的存储类型为redis，也可以为null，则什么都没有
    SESSION_REDIS = Redis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_REDIS.ping()
    print('redis is ',SESSION_REDIS)
except:
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)),'sessions')
    print('-----------------------', SESSION_FILE_DIR)

SESSION_USE_SIGNER = True ##是否强制加盐，混淆session, 使用的话必须要有secret_key
SESSION_PERMANENT =False #sessons是否长期有效，false，则关闭浏览器，session失效
PERMANENT_SESSION_LIFETIME = 3600 #session长期有效，则设定session生命周期，整数秒，默认大概不到3小时

#解决flask 中返回json请求的时候中文编码的问题，主要是requests.post的时候发生的，类似json.dumps(data, ensure_ascii=False)
JSON_AS_ASCII = False

#热更新html模板文件,修改了静态文件后不需要重启就可生效
TEMPLATES_AUTO_RELOAD = True

# Json config
#app_path = os.path.realpath(os.path.dirname(__file__))
JSON_CONFIG_PATH = BASE_DIR+"\\app\\data\\appconfig.json"

#配置Celery 分布式的消息队列处理系统
CELERY_BROKER_URL = "redis://{}:{}/0".format(REDIS_HOST, REDIS_PORT)
CELERY_RESULT_BACKEND = "redis://{}:{}/0".format(REDIS_HOST, REDIS_PORT)


