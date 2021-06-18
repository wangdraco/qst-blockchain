# coding: utf-8
from threading import Lock
from app import socketio,app
import json,threading



temp_thread = None
tower_thread = None
mqtt_thread = None
elec_thread = None
water_thread = None
thread_lock = Lock()

#web socket listner
@socketio.on('connect', namespace='/ws/main')
def on_connect():
    print('ws/main namespace  connected..................')

    # start a background thread
    # global temp_thread,tower_thread,mqtt_thread,elec_thread,water_thread
    # with thread_lock:
    #     if temp_thread is None:
    #         temp_thread = socketio.start_background_task(target=background_temp_thread)


@socketio.on('connect', namespace='/ws/index')
def on_connect_index():
    print('ws/index namespace  connected..................')


#temp and humidity data in background thread
def background_temp_thread():
    """Example of how to send server generated events to clients. must use socketio.emit to send data"""
    _temp_data = {}
    _temp_data['temp'] = 12.5
    _temp_data['humi'] = 72.3

    while True:
        socketio.emit('temp_data', {'data': json.dumps(_temp_data,ensure_ascii=False)}, namespace='/ws/main')
        print('发送到页面的--杨尘数据===================', json.dumps(_temp_data,ensure_ascii=False))
        socketio.sleep(5)



@app.route('/test/socketio/<namespace>')
def test_socket(namespace):
    _namespace = f'/ws/{namespace}'
    socketio.emit('temp_data', {'data': 'dddddd'}, namespace=_namespace)
    socketio.sleep(2)#同时发送消息的时候，必须有个时间间隔
    # socketio.emit('alert_data', {'data': 'eeee'}, namespace='/ws/main')

    _data = {'data': 'threading data'}
    t = threading.Thread(target=websocket_thread,
                         kwargs={'event_id': 'temp_data', 'data': _data, 'namespace':_namespace})
    t.start()

    return 'send socket successful'

def websocket_thread(**data):
    event_id = data['event_id']
    _data = data['data']
    _namespace = data['namespace']
    print('begin emit data---------------',_data)
    socketio.emit(event_id, _data, namespace=_namespace)
    socketio.sleep(2)  # 同时发送消息的时候，必须有个时间间隔
