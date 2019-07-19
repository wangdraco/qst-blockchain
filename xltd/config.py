# Statement for enabling the development environment,
# 引用方式: app.config.from_object('config'), config.py里面的 key必须是大写的,
#很多地方就不用写配置了, 比如debug=True, SECRET_KEY等,系统自动从下面取值
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'clouddata.db')
#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://energy:energy168@139.129.200.70/clouddata?charset=utf8'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://energy:energy168@127.0.0.1/clouddata?charset=utf8'
DATABASE_CONNECT_OPTIONS = {}

#数据库连接池的大小。默认是引擎默认值（通常 是 5 ）
SQLALCHEMY_POOL_SIZE = 50

#指定数据库连接池的超时时间。默认是 10
SQLALCHEMY_POOL_TIMEOUT = 15

#自动回收连接的秒数, 如果使用 MySQL 的话， Flask-SQLAlchemy 会自动地设置这个值为 2 小时
SQLALCHEMY_POOL_RECYCLE = 3600

#控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃
SQLALCHEMY_MAX_OVERFLOW = 60

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
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "admin168."

# Secret key for signing cookies
SECRET_KEY = "!@#qwer$%^"

#解决flask 中返回json请求的时候中文编码的问题，主要是requests.post的时候发生的，类似json.dumps(data, ensure_ascii=False)
JSON_AS_ASCII = False

# Json config
#app_path = os.path.realpath(os.path.dirname(__file__))
JSON_CONFIG_PATH = BASE_DIR+"\\app\\data\\appconfig.json"

#block chain node id
BLOCKCHAIN_IP = "192.168.1.4"
BLOCKCHAIN_PORT = 9002
