import pymysql
from collections import Counter
import operator
import itertools
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "localhost")
DB_PASS = os.getenv("DB_PASS", "localhost")
DB_DATABASE = os.getenv("DB_DATABASE", "localhost")

def get_connection():
    return pymysql.connect(DB_HOST,DB_USER, DB_PASS, DB_DATABASE, cursorclass=pymysql.cursors.DictCursor)

connection = get_connection()

def create_post_record(post):
    if check_post_exists_by_slug(post["slug"]):
        return
    with connection.cursor() as cursor:
        sql = """INSERT INTO kodilan_posts(slug, position, location, created_at, company, tags, description)VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(sql, (post.get('slug'), post.get('position'), post.get('location'), post.get('created_at'), post.get('company'), post.get('tags'), post.get('description')))
        connection.commit()

def check_post_exists_by_slug(slug):
    with connection.cursor() as cursor:
        sql = "SELECT slug FROM kodilan_posts WHERE slug=%s"
        cursor.execute(sql, (slug))
        return cursor.fetchone() is not None

def get_location_stats(startDate, endDate, order = "desc"):
    with connection.cursor() as cursor:
        where = f'where `created_at` >= %s && `created_at` <= %s'
        sql = f'SELECT location, count(*) as toplam_ilan_sayisi from kodilan_posts {where} group by location order by toplam_ilan_sayisi {order};'
        cursor.execute(sql, (startDate, endDate))
        result = cursor.fetchall()
        return result

def get_company_stats(startDate, endDate, order = "desc"):
    with connection.cursor() as cursor:
        where = f'where `created_at` >= %s && `created_at` <= %s'
        sql = f'SELECT company, count(*) as toplam_ilan_sayisi from kodilan_posts {where} group by company order by toplam_ilan_sayisi {order};'
        cursor.execute(sql, (startDate, endDate))
        return cursor.fetchall()

def get_all(startDate, endDate, order = "desc"):
    with connection.cursor() as cursor:
        where = f'where `created_at` >= %s && `created_at` <= %s'
        sql = f'SELECT * from kodilan_posts {where} order by id {order};'
        cursor.execute(sql, (startDate, endDate))
        return cursor.fetchall()

def get_position_stats(startDate, endDate, order = "desc"):
    with connection.cursor() as cursor:
        where = f'where `created_at` >= %s && `created_at` <= %s'
        sql = f'SELECT position, count(*) as toplam_ilan_sayisi from kodilan_posts {where} group by position order by toplam_ilan_sayisi {order};'
        cursor.execute(sql, (startDate, endDate))
        result = cursor.fetchall()
        return result

def get_lang_stats(startDate, endDate, order = "desc"):
    langs = ["java", "c#", "python", "javascript", "go", "dart", "php", "ruby"]
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
    langs = ["spring", "django", "rails", "laravel", "express", "flask", "rails", "dotnet"]
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
    langs = ["react", "vue", "jquery", "bootstrap", "angular", "redux", "vuex", "figma"]
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
    with connection.cursor(cursor=pymysql.cursors.Cursor) as cursor:
        sql = "SELECT * from kodilan_tags"
        cursor.execute(sql)
        flatten = itertools.chain.from_iterable
        return list(flatten(cursor.fetchall()))

def get_descriptions(startDate, endDate, order = "desc"):
    with connection.cursor() as cursor:
        where = f'where `created_at` >= %s && `created_at` <= %s'
        sql = f'SELECT description from kodilan_posts {where};'
        cursor.execute(sql, (startDate, endDate))
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