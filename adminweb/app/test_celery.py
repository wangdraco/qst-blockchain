from app.mod_celerytask.tasks import run_one_task
import time
from celery.result import AsyncResult
# from celery import Celery
#
# #use Celery as task queue!!
# celery = make_celery(app)
#
# # celery = Celery(
# #         'testtask',
# #         backend='redis://127.0.0.1:6379/0',
# #         broker='redis://127.0.0.1:6379/0'
# #     )
#
# @celery.task(base=CallbackTask)
# def run_one_task(arg1, arg2):
#     print('begin additon arg1 + arg2')
#     time.sleep(5)
#
#     return arg1 + arg2
#
def call_task():
    _result = run_one_task.apply_async(args=[12,23])

    return _result

# celery.send_task('testtask',args=[12,23])

result = call_task()

while True:
    print('ready ?? ',result.ready())
    if result.ready():
        print(f'result is {result.get()}')
        break
    time.sleep(1)
