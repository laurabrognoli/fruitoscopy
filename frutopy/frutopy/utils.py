import sqlite3
import psycopg2
import os
from django.conf import settings
from datetime import datetime


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
    print("before rows")
    for row in rows:
        a = "'{" + row[1] + "}'"
        print(row[8])
        try:
            img = os.path.join(folder_name, row[8])
        except AttributeError:
            img = ""
        print(img)
        cur.execute(
            """INSERT INTO %s (spectrum, fruit, label, gps, tmstp, ml_model_id, sp_model_id, image_path) VALUES (%s, %d, %d, '%s', '%s', %d, %d, '%s');"""
            % (table_name, a, row[2], row[3], row[4], datetime.fromtimestamp(row[5]), row[6]+1, row[7]+1, img))
    cur.execute("COMMIT;")