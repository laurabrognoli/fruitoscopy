import sqlite3
import psycopg2
from django.conf import settings
from datetime import datetime
import frutopy.tasks
import time
import os
import shutil


def handle_uploaded_file(f):
    """
    Handles uploaded file and triggers its processing (celery task).
    """
    file_name = str(int(time.time()))
    # ^ okay so what if two people upload two files at the same time? idk
    full_path = os.path.join(settings.IMG_TMP_PATH, file_name)
    os.makedirs(full_path)
    with open(full_path + '/tmp_file.gz', 'wb') as fd:
        for chunk in f.chunks():
            fd.write(chunk)
    file_full_path = os.path.join(full_path, 'tmp_file.gz')
    print(full_path)
    frutopy.tasks.process_file.delay(file_full_path, full_path)
    #TODO: return something to deal with errors (set ignore on task to false!)


def get_dir(dest):
    print(dest)
    for root, dirs, files in os.walk(dest):
        print(dirs)
        return dirs[0], os.path.join(dest, dirs[0])


def read_db(db_name, table_name='Samples'):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute("select * from {}".format(table_name))
    my_table = cur.fetchall()
    conn.close()
    return my_table


def process_image(image_path):
    """
    Takes image path
    """


def write_central_db(rows, folder_name):
    conn = psycopg2.connect(settings.DB_PARAMS_CONNECT)
    cur = conn.cursor()
    table_name = 'frutopy_sample'
    cur.execute("BEGIN;")
    for row in rows:
        a = "'{" + row[1] + "}'"
        try:
            img = os.path.join(folder_name, row[8])
        except AttributeError:
            img = ""
        cur.execute(
            """INSERT INTO %s (spectrum, fruit, label, gps, tmstp, ml_model_id, sp_model_id, image_path) VALUES (%s, %d, %d, '%s', '%s', %d, %d, '%s');"""
            % (table_name, a, row[2], row[3], row[4], datetime.fromtimestamp(row[5]), row[6]+1, row[7]+1, img))
    cur.execute("COMMIT;")