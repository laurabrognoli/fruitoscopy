import os
import shutil
import tarfile
import tempfile
from frutopy.celery import app
from django.conf import settings

from frutopy.utils import write_central_db, read_db, get_dir


@app.task(ignore_result=True)
def process_file(file_path):
    """
    Untar file and process SQLite database to update main PostgreSQL database
    """
    print("File path: %s" % file_path)
    tfile = tarfile.open(file_path)
    with tempfile.TemporaryDirectory() as destination:
        tfile.extractall(destination)
        print(os.listdir(destination))
        a = get_dir(destination)
        shutil.move(a[1], settings.MEDIA_ROOT)
        write_central_db(read_db(os.path.join(destination, settings.INPUT_DB)), os.path.join(settings.MEDIA_URL, a[0]))
        os.remove(file_path)

