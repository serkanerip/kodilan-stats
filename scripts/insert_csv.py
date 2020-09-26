import pymysql
from collections import Counter
import operator
import itertools
import csv_utils

connection = pymysql.connect("localhost","root","toor","development",cursorclass=pymysql.cursors.DictCursor)

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

delete_old_tags()
for tag in csv_utils.get_tags_from_csv('tags2.csv'):
    insert_tag(tag)
