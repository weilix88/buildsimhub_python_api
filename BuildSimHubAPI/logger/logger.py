import os
import datetime as dt
import threading
import csv
import os.path

global_lock = threading.Lock()


def threaded(fn):
    while global_lock.locked():
        continue
    global_lock.acquire()

    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
        global_lock.release()
    return wrapper


class BuildSimLogger(object):
    logger_csv_name = 'buildsim_logger.csv'

    def __init__(self, logger_dir=None):
        # some initial value
        if logger_dir is None:
            self.logger_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.logger_content = []

        if not os.path.isfile(self.logger_dir + '/buildsim_logger.csv'):
            f = open(self.logger_dir + '/buildsim_logger.csv', 'w+')
            f.write("Time, Class, Request, ProjectAPI, ModelAPI, ResponseCode, Results \n")
            f.close()

    def write_in_message(self, class_name='', request='', project_id='', model_id='', code=200, result=''):
        logger_msg = [dt.datetime.now().strftime('%y/%m/%d %H:%M:%S'), class_name, request, project_id,
                      model_id, str(code), result]
        self.logger_content.append(logger_msg)

    @threaded
    def write_in_csv(self):
        with open(self.logger_dir + '/buildsim_logger.csv', "a+") as file:
            csv_writer = csv.writer(file, delimiter=',')
            csv_writer.writerows(self.logger_content)
