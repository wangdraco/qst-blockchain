from celery import Celery, Task
import logging


from celery.worker.request import Request


# 必须在命令行启动 celery worker -A app.celery --loglevel=info
# 在app目录的上层目录运行
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['app.mod_celerytask.tasks']
    )
    celery.conf.update(app.config,
                       BROKER_TRANSPORT_OPTIONS={
                           "visibility_timeout": 36000,
                           'max_retries': 5
                        },
                       CELERY_TASK_SERIALIZER='json',
                       CELERY_TIMEZONE='Asia/Shanghai')

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


logger = logging.getLogger('my.package')


class MyRequest(Request):
    'A minimal custom request to log failures and hard time limits.'

    def on_timeout(self, soft, timeout):
        super(MyRequest, self).on_timeout(soft, timeout)

        if not soft:
            logger.warning(

                'A hard timeout was enforced for task %s',

                self.task.name

            )

    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        super(Request, self).on_failure(

            exc_info,

            send_failed_event=send_failed_event,

            return_ok=return_ok

        )

        logger.warning(

            'Failure detected for task %s',

            self.task.name

        )

    def on_success(self, retval, task_id, args, kwargs):
        super(Request, self).on_success(

            retval,
            task_id = task_id,
            args = args,
            kwargs = kwargs
        )
        print('successful ======,',retval, '__',task_id)
        logger.info(

            'succeed detected for task %s',

            self.task.name

        )

class CallbackTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        '''成功执行的函数'''
        print(f"callback success function,====and result is {retval}, id is {task_id}")
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        '''失败执行的函数'''
        print(f"callback failure function ,and info is {einfo}")


class MyTask(Task):
    Request = MyRequest  # you can use a FQN 'my.package:MyRequest'
