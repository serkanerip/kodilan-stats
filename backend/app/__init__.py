import flask
import os
import pymysql
from flask import request, jsonify, g
from flask_cors import CORS
from app.routes.stats import stats_api


app = flask.Flask(__name__)
app.config.from_pyfile('config.py')
CORS(app)


def get_connection():
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "")
    DB_PASS = os.getenv("DB_PASS", "")
    DB_DATABASE = os.getenv("DB_DATABASE", "kodilan_stats")
    if not hasattr(g, 'db'):
        g.db = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_DATABASE, cursorclass=pymysql.cursors.DictCursor)
    return g.db


app.register_blueprint(stats_api)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()
