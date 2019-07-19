from app import app,socketio,mc
import eventlet
from eventlet import wsgi





pool = eventlet.greenpool.GreenPool() #default size=1000
listener = eventlet.listen(('127.0.0.1',5000))
wsgi.server(listener, app,socket_timeout=30,custom_pool=pool,keepalive=False)

#socketio.run(app,host='127.0.0.1',debug=True,port=5000,socket_timeout=30,custom_pool=pool)



