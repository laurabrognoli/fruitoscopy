# from __future__ import absolute_import
#
# from celery import Celery
# import tempfile
# import tarfile
# import os
# import shutil
# from django.conf import settings
# from utils import write_central_db, read_db, get_dir
#
#
# app = Celery('tasks', backend='amqp', broker='amqp://')
#
#
# @app.task(ignore_result=True)
# def process_file(file_path):
#     """
#     Untar file and process SQLite database to update main PostgreSQL database
#     """
#     print("File path: %s" % file_path)
#     tfile = tarfile.open(file_path, 'r:gz')
#     with tempfile.TemporaryDirectory() as destination:
#         tfile.extractall(destination)
#         shutil.move(get_dir(destination)[1], settings.MEDIA_ROOT)
#         write_central_db(read_db(os.path.join(destination, settings.INPUT_DB)), os.path.join(settings.MEDIA_URL, destination[0]))
#         print(os.path.join('/tables/static/images', destination[0]))


from __future__ import absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frutopy.settings')

from django.conf import settings  # noqa

app = Celery('frutopy')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))