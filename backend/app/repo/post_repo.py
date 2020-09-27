import pymysql
from collections import Counter
import operator
import itertools
import os
from app import get_connection

def run_query(query, binds=None, cursor_type=pymysql.cursors.DictCursor) -> pymysql.cursors.Cursor:
    connection = get_connection()
    cursor = connection.cursor(cursor_type)
    if (binds is None):
        cursor.execute(query)
    else:
        cursor.execute(query, binds)
    connection.commit()
    return cursor

def create_post_record(post):
    if check_post_exists_by_slug(post["slug"]):
        return
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = """INSERT INTO kodilan_posts(slug, position, location, created_at, company, tags, description)VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (post.get('slug'), post.get('position'), post.get('location'), post.get('created_at'), post.get('company'), post.get('tags'), post.get('description')))
        connection.commit()

def check_post_exists_by_slug(slug):
    cursor = run_query("SELECT slug FROM kodilan_posts WHERE slug=%s", binds=(slug))
    return cursor.fetchone() is not None

def get_location_stats(startDate, endDate, order = "desc"):
    where = f'where `created_at` >= %s && `created_at` <= %s'
    sql = f'SELECT location, count(*) as toplam_ilan_sayisi from kodilan_posts {where} group by location order by toplam_ilan_sayisi {order};'
    with run_query(sql, (startDate, endDate)) as cursor:
        return cursor.fetchall()

def get_company_stats(startDate, endDate, order = "desc"):
    where = f'where `created_at` >= %s && `created_at` <= %s'
    sql = f'SELECT company, count(*) as toplam_ilan_sayisi from kodilan_posts {where} group by company order by toplam_ilan_sayisi {order};'
    with run_query(sql, (startDate, endDate)) as cursor:
        return cursor.fetchall()

def get_all(startDate, endDate, order = "desc"):
    where = f'where `created_at` >= %s && `created_at` <= %s'
    sql = f'SELECT * from kodilan_posts {where} order by id {order};'
    with run_query(sql, (startDate, endDate)) as cursor:
        return cursor.fetchall()

def get_position_stats(startDate, endDate, order = "desc"):
    where = f'where `created_at` >= %s && `created_at` <= %s'
    sql = f'SELECT position, count(*) as toplam_ilan_sayisi from kodilan_posts {where} group by position order by toplam_ilan_sayisi {order};'
    with run_query(sql, (startDate, endDate)) as cursor:
        return cursor.fetchall()

def get_lang_stats(startDate, endDate, order = "desc"):
    connection = get_connection()
    langs = ["java", "c#", "python", "javascript", "go", "dart", "php", "ruby", "c", "c++", "typescript"]
    with connection.cursor() as cursor:
        res = []
        for lang in langs:
            where = f'where (tags like %s or tags like %s) && `created_at` >= %s && `created_at` <= %s'
            sql = f'select %s as lang,count(*) as total from kodilan_posts {where}'
            cursor.execute(sql, (lang, f'%{lang}', f'%{lang},%', startDate, endDate))
            res.append(cursor.fetchone())
        res.sort(key = operator.itemgetter('total'), reverse=True)
        return res

def get_tech_stats(startDate, endDate, order = "desc"):
    connection = get_connection()
    langs = ["spring", "django", "nodejs", "react", "vue", "react-native", "flutter", "rails", "dotnet", "laravel"]
    with connection.cursor() as cursor:
        res = []
        for lang in langs:
            where = f'where (tags like %s or tags like %s) && `created_at` >= %s && `created_at` <= %s'
            sql = f'select %s as tech, count(*) as total from kodilan_posts {where}'
            cursor.execute(sql, (lang, f'%{lang}', f'%{lang},%', startDate, endDate))
            res.append(cursor.fetchone())
        res.sort(key = operator.itemgetter('total'), reverse=True)
        return res


def get_web_framework_stats(startDate, endDate, order = "desc"):
    connection = get_connection()
    langs = ["spring", "django", "rails", "laravel", "express", "flask", "dotnet", "asp.net", "jsp", "symfony"]
    with connection.cursor() as cursor:
        res = []
        for lang in langs:
            where = f'where (tags like %s or tags like %s) && `created_at` >= %s && `created_at` <= %s'
            sql = f'select %s as tech, count(*) as total from kodilan_posts {where}'
            cursor.execute(sql, (lang, f'%{lang}', f'%{lang},%', startDate, endDate))
            res.append(cursor.fetchone())
        res.sort(key = operator.itemgetter('total'), reverse=True)
        return res

def get_front_end_tech_stats(startDate, endDate, order = "desc"):
    connection = get_connection()
    langs = ["react", "vue", "jquery", "bootstrap", "angular", "redux", "vuex", "figma", "photoshop"]
    with connection.cursor() as cursor:
        res = []
        for lang in langs:
            where = f'where (tags like %s or tags like %s) && `created_at` >= %s && `created_at` <= %s'
            sql = f'select %s as tech, count(*) as total from kodilan_posts {where}'
            cursor.execute(sql, (lang, f'%{lang}', f'%{lang},%', startDate, endDate))
            res.append(cursor.fetchone())
        res.sort(key = operator.itemgetter('total'), reverse=True)
        return res

def get_tags():
    sql = "SELECT * from kodilan_tags"
    with run_query(sql, cursor_type=pymysql.cursors.Cursor) as cursor:
        flatten = itertools.chain.from_iterable
        return list(flatten(cursor.fetchall()))

def get_descriptions(startDate, endDate, order = "desc"):
    where = f'where `created_at` >= %s && `created_at` <= %s'
    sql = f'SELECT description from kodilan_posts {where};'
    with run_query(sql, (startDate, endDate)) as cursor:
        return cursor.fetchall()

def get_descriptions_and_tags(startDate, endDate, order = "desc"):
    where = f'where `created_at` >= %s && `created_at` <= %s'
    sql = f'SELECT description, tags from kodilan_posts {where};'
    with run_query(sql, (startDate, endDate)) as cursor:
        return cursor.fetchall()

def get_related_tag(allTags, tag):
    tagsSum = ""
    for result in allTags:
        if result["tags"].find(tag) != -1:
            tagsSum += result["tags"].replace(tag, '')
    tagsArr = tagsSum.split(",")
    mostWords = Counter(tagsArr)
    rels = []
    for tup in mostWords.most_common(4):
        if len(tup[0]) > 0:
            rels.append(tup[0])
    return ",".join(rels)