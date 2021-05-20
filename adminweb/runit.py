from app import app,socketio
import eventlet






if __name__ == "__main__":

    #普通运行方式，没有socketio功能
    # app.run(host='127.0.0.1', port=5000)


    # 在没有gunicorn的机器上， 要使用socketio，必须使用eventlet.monkey_patch()，
    #在linux系统中，如果使用gunicorn就不用monkey_patch,直接使用gunicorn -c gunicorn.py runit:app
    eventlet.monkey_patch()

    pool = eventlet.greenpool.GreenPool()  # default size=1000
    socketio.run(app, host='127.0.0.1', debug=False, port=5000, socket_timeout=30, custom_pool=pool)
    # socketio.run(app, host='127.0.0.1', debug=False, port=5000)




