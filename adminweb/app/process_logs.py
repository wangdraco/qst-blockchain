import os,logging
from logging.handlers import RotatingFileHandler

class log_class():
    def __init__(self,_app, _debug, _path, _logname, _max, _backup):
        if not _debug:
            if not os.path.exists(_path):
                print(f'created log file path==========={_path}===========================')
                os.mkdir(_path)
            self._app = _app
            self.file_handler = RotatingFileHandler(f'{_path}/{_logname}.log', maxBytes=_max,
                                                       backupCount=_backup)

            self._app.logger.addHandler(self.file_handler)


    def info(self, _info):
        self._app.logger.setLevel(logging.INFO)
        self.file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '))
        self._app.logger.info(_info)

    def error(self,_error):
        self.file_handler.setLevel(logging.ERROR)
        self.file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
