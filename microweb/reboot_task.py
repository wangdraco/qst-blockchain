import machine

def call_reset():
  print('begin restart---')
  machine.reset()

def run():
    tim1 = machine.Timer(1)
    tim1.init(period=2000, mode=machine.Timer.ONE_SHOT, callback=lambda t: call_reset())

run()