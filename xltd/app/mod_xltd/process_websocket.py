# coding: utf-8
from threading import Lock
from app import socketio,get_memcache
import json,requests


mc = get_memcache()
thread = None
tower_thread = None
mqtt_thread = None
elec_thread = None
water_thread = None
thread_lock = Lock()

#web socket listner
@socketio.on('connect', namespace='/xltd-daping')
def on_connect():
    print('dust web connected..................')

    # start a background thread
    global thread,tower_thread,mqtt_thread,elec_thread,water_thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_dust_thread)

        if tower_thread is None:
            tower_thread = socketio.start_background_task(target=background_tower_thread)

        if elec_thread is None:
            elec_thread = socketio.start_background_task(target=background_electronic_thread)

        if water_thread is None:
            water_thread = socketio.start_background_task(target=background_water_thread)
        #
        # if mqtt_thread is None:
        #     mqtt_thread = socketio.start_background_task(target=background_thread_mqtt)



#temp and humidity data in background thread
def background_dust_thread():
    """Example of how to send server generated events to clients. must use socketio.emit to send data"""
    while True:
        if mc and mc.get('xltd_dust') is not None:
            socketio.emit('dust_data', {'data': mc.get('xltd_dust')}, namespace='/xltd-daping')
            print('发送到页面的--杨尘数据===================', mc.get('xltd_dust'))
        socketio.sleep(15)


#tower crane data thread
def background_tower_thread():
    while True:
        if mc and mc.get('xltd_tower') is not None:
            socketio.emit('tower_data', {'data': mc.get('xltd_tower')}, namespace='/xltd-daping')
            print('发送到页面的塔吊数据===================',mc.get('xltd_tower'))
        socketio.sleep(20)


#eletronic data collection
def background_electronic_thread():
    while True:
        if mc and mc.get('xltd_electronic') is not None:
            socketio.emit('electronic_data', {'data': mc.get('xltd_electronic')}, namespace='/xltd-daping')
        socketio.sleep(25)

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