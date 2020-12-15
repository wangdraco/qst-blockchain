import _thread,time

def test_print(s,t):
    while True:
        print('hello------')
        time.sleep(s)

try:
    _thread.start_new_thread(test_print, (2,2))
except Exception as e:
    print(e)


