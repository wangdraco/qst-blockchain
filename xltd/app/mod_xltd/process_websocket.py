# coding: utf-8
from threading import Lock
from app import socketio,get_memcache
import json

mc = get_memcache()
thread = None
tower_thread = None
mqtt_thread = None
thread_lock = Lock()

#web socket listner
@socketio.on('connect', namespace='/xltd-daping')
def on_connect():
    print('dust web connected..................')

    # start a background thread
    global thread,tower_thread,mqtt_thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_dust_thread)

        if tower_thread is None:
            tower_thread = socketio.start_background_task(target=background_tower_thread)
        #
        # if mqtt_thread is None:
        #     mqtt_thread = socketio.start_background_task(target=background_thread_mqtt)



#temp and humidity data in background thread
def background_dust_thread():
    """Example of how to send server generated events to clients. must use socketio.emit to send data"""
    while True:
        if mc and mc.get('xltd_dust') is not None:
            socketio.emit('dust_data', {'data': mc.get('xltd_dust')}, namespace='/xltd-daping')
        socketio.sleep(15)


#tower crane data thread
def background_tower_thread():
    while True:
        if mc and mc.get('xltd_tower') is not None:
            socketio.emit('tower_data', {'data': mc.get('xltd_tower')}, namespace='/xltd-daping')
        socketio.sleep(20)
