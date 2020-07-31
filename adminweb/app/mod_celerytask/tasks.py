from app import app, celery
from app.process_celery import CallbackTask
import time
from flask import jsonify
#root@iZclsuc6keq1xwZ:/usr/local/adminweb# celery worker -A app.celery --loglevel=info

@celery.task(base=CallbackTask)
def run_one_task(arg1, arg2):
    print('begin additon arg1 + arg2')
    time.sleep(5)

    return arg1 + arg2


@celery.task(base=CallbackTask)
def my_background_task(arg1, arg2):
    print('begin additon arg1 + arg2')
    time.sleep(20)

    return arg1 + arg2

@app.route('/celery/calltask')
def call_task():
    _result = my_background_task.apply_async([300, 200])
    return _result.id

@app.route('/celery/result/<taskid>')
def result_celery(taskid):

    _result = celery.AsyncResult(taskid)

    print('result is =====',_result.result)
    print('the task is ===',_result.status)
    return str(_result.result)

@app.route('/celery/status/<task_id>')
def taskstatus(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)