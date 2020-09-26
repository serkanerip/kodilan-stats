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

for tag in csv_utils.get_tags_from_csv('tags2.csv'):
    insert_tag(tag)
