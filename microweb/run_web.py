from main_web import app


def run_web():
    # app.run(host='192.168.3.155', port=80,debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)

try:
    import threading
    threading.Thread(target=run_web).start()
except:
    print('import threading error!!!')
    import _thread
    _thread.start_new_thread(run_web, ())


# import _thread,threading
#
#
#
# threading.Thread(target=run_web).start()
# print('dddddddddddddd')
#_thread.start_new_thread(run_web, ())