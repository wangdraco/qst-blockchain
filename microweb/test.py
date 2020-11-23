#--demo decorator function-----
# import time
#
# def deco(func):
#     start_time = time.time()
#     func()
#     end_time = time.time()
#     execution_time = (end_time - start_time)*1000
#     print("time is %d ms" %execution_time)
#
# def f():
#     print("hello")
#     time.sleep(1)
#     print("world")
#
# if __name__ == '__main__':
#
#     deco(f)
#     print("f.__name__ is",f.__name__)
#     print()



import time

class Decor():
    def __init__(self):
        pass

    def deco(self,func):
        def wrapper(a,b):
            start_time = time.time()
            func(a,b)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            print("time is %d ms" % execution_time)
        return wrapper

d = Decor()

@d.deco
def f(a,b):
    print("hello",a,'--',b)
    time.sleep(1)
    print("world")

if __name__ == '__main__':
    f(2,3)