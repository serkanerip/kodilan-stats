import pymysql
from collections import Counter
import operator
import itertools
import csv_utils
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")
DB_DATABASE = os.getenv("DB_DATABASE", "kodilan_stats")

connection = pymysql.connect(DB_HOST,DB_USER, DB_PASS, DB_DATABASE, cursorclass=pymysql.cursors.DictCursor)


def insert_tag(tag):
    with connection.cursor() as cursor:
        sql = "INSERT INTO kodilan_tags VALUES(%s)"
        cursor.execute(sql, (tag))
        connection.commit()


def delete_old_tags():
    with connection.cursor() as cursor:
        sql = "DELETE FROM kodilan_tags WHERE 1"
        cursor.execute(sql)
        connection.commit()


with open('tags.csv', 'r') as reader:
    content = reader.read()
    for tag in content.split('\n'):
        insert_tag(tag)
