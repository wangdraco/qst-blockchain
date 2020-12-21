import machine
import config as conf

def call_reset():
  print('begin restart---')
  machine.reset()

tim0 = machine.Timer(0)
tim0.init(period=conf.restart_time, mode=machine.Timer.PERIODIC, callback=lambda t: call_reset())
print('call timer task--------------')