import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import time
import sqlite3 as lite
import numpy as np

HOME_PATH  = os.path.dirname(os.path.abspath(__file__))

def configure_wl():
    pass
