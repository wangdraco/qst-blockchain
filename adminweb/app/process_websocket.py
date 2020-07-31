# coding: utf-8
from threading import Lock
from app import socketio
import json,requests


thread = None
tower_thread = None
mqtt_thread = None
elec_thread = None
water_thread = None
thread_lock = Lock()

#web socket listner
@socketio.on('connect', namespace='/test')
def on_connect():
    print('index web connected..................')

    # start a background thread
    global thread,tower_thread,mqtt_thread,elec_thread,water_thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_dust_thread)

        #if tower_thread is None:
        #    tower_thread = socketio.start_background_task(target=background_tower_thread)

        #if elec_thread is None:
        #    elec_thread = socketio.start_background_task(target=background_electronic_thread)

        #if water_thread is None:
        #    water_thread = socketio.start_background_task(target=background_water_thread)
        #
        # if mqtt_thread is None:
        #     mqtt_thread = socketio.start_background_task(target=background_thread_mqtt)

@socketio.on('disconnect', namespace='/test')
def on_disconnect():

    print('index web disconnected!!!!!')

@socketio.on('web_message',  namespace='/test')
def handle_message(message):
    print('received message from web: ', message)

#temp and humidity data in background thread
def background_dust_thread():
    """Example of how to send server generated events to clients. must use socketio.emit to send data"""
    while True:
        #if mc and mc.get('xltd_dust') is not None:
        socketio.emit('test_data', {'data': 'this is a test message'}, namespace='/test')
        print('发送到页面的--测试数据===================', ' and the is_coonected is =')
        socketio.sleep(5)



#直接从云服务器上取水数
def background_water_thread():
    while True:
        water_url = 'http://139.129.200.70:5000/device/db-9198,514,2'

        try:
            _data = {}
            r1 = requests.get(water_url)
            _data['db-9198-514']=r1.json()['db-9198-514']
            socketio.emit('water_data', {'data': json.dumps(_data,ensure_ascii=False)}, namespace='/xltd-daping')
            print('final 水表数据是 ==========',_data)
            socketio.sleep(23)

        except Exception as e:
            print('取水表数据出错', e)
            socketio.sleep(5)