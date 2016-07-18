import os
import shutil
import tarfile
import tempfile
from frutopy.celery import app
from django.conf import settings
import frutopy.utils
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@app.task(ignore_result=True)
def process_file(file_path, dir_path):
    """
    Untars file and processes SQLite database to update main PostgreSQL database.
    """
    try:
        tfile = tarfile.open(file_path)
        with tempfile.TemporaryDirectory() as destination:
            tfile.extractall(destination)
            a = frutopy.utils.get_dir(destination)
            shutil.move(a[1], settings.MEDIA_ROOT)
            input_db_path = os.path.join(destination, settings.INPUT_DB)
            image_folder_name = os.path.join(settings.MEDIA_URL, a[0])
            frutopy.utils.write_central_db(frutopy.utils.read_db(input_db_path), image_folder_name)
        logger.info("Success")
    except Exception as e:
        logger.error(e)
    finally:
        shutil.rmtree(dir_path)

@app.task()
def check_model():
    query = Sample.objects.filter(label_is_right=True)
    data_matrix = np.array(query[0].spectrum)
    labels = np.array(query[0].label)
    for q in query[1:]:
        np.concatenate(data_matrix, q.spectrum, axis=1)
        np.append(labels, q.label)
