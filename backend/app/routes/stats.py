import itertools
from datetime import date
from flask import request, Blueprint, g
from app import app
from collections import Counter
from app.repo import post_repo
from app.business import tags_finder
from app.interfaces import kodilan_client

stats_api = Blueprint('stats', __name__, url_prefix="/api/v1")

def getTagList():
    if (not hasattr(g, 'tl')):
        g.tl = post_repo.get_tags()
    return g.tl

@app.route("/api/v1/setupposts")
def setupPosts():
    posts = kodilan_client.getPosts()
    for post in posts:
        post_repo.create_post_record(post)
    return { 'message': 'Success!' }

@app.route("/api/v1/extracttags")
def tag():
    text = request.form.get('text', type = str)
    if (text is None):
        return { 'data': []}
    return { 'data': tags_finder.exportTagsFromText(text, getTagList()) }


@app.route("/api/v1/stats/tag")
def tagStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    limit = request.args.get('limit', default = 10, type = int)
    descriptions = post_repo.get_descriptions(startDate=startDate, endDate=endDate, order=order)
    allPostTags = []
    for result in descriptions:
        allPostTags.append(tags_finder.exportTagsFromText(result["description"], getTagList()))
    allPostTags = itertools.chain.from_iterable(allPostTags) # flat list
    mostTags = []
    counter = Counter(allPostTags)
    if limit < 1 or limit >= counter.__len__():
        limit = 10
    for tup in counter.most_common(limit):
        mostTags.append({
            'tag': tup[0],
            'count': tup[1]
        })
    return {
        'data': mostTags
    }

@app.route("/api/v1/posts")
def getAll():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': post_repo.get_all(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/location")
def locStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': post_repo.get_location_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/company")
def compStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': post_repo.get_company_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/position")
def posStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': post_repo.get_position_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/lang")
def langStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': post_repo.get_lang_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/tech")
def techStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': post_repo.get_web_framework_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/web")
def wfStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': post_repo.get_web_framework_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/frontend")
def fendStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': post_repo.get_front_end_tech_stats(startDate=startDate, endDate=endDate, order=order)
    }
