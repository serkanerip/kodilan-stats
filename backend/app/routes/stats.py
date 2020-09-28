import itertools
from datetime import date
from flask import request, Blueprint, g, session
from app import app
from collections import Counter
from app.repo import post_repo
from app.business import tags_finder
from app.interfaces import kodilan_client

stats_api = Blueprint('stats', __name__, url_prefix="/api/v1")
tagsList = list = []
tagsListCounter = dict = {}


@app.before_first_request
def t():
    global tagsList
    tagsList = post_repo.get_tags()


@stats_api.route("/setupposts")
def setupPosts():
    posts = kodilan_client.getPosts()
    for post in posts:
        post_repo.create_post_record(post)
    return {'message': 'Success!'}


@stats_api.route("/extracttags", methods=["GET", "POST"])
def tag():
    text = request.form.get('text', type=str)
    if (text is None):
        return {'data': []}
    return {'data': tags_finder.export_tags_from_text(text, tagsList)}


def get_tags_from_descriptions(startDate, endDate, order):
    if (f'{startDate}-{endDate}' in tagsListCounter):
        return tagsListCounter[f'{startDate}-{endDate}']
    descriptions = post_repo.get_descriptions_and_tags(startDate=startDate, endDate=endDate, order=order)
    allPostTags = []
    for result in descriptions:
        postContent = result["description"] + "\n" + result["tags"]
        allPostTags.append(tags_finder.export_tags_from_text(postContent, tagsList))
    counter = Counter(itertools.chain.from_iterable(allPostTags)) # flat list
    tagsListCounter[f'{startDate}-{endDate}'] = counter
    return counter


@app.route("/api/v1/stats/tag")
def tagStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    limit = request.args.get('limit', default = 10, type = int)
    allPostTags = get_tags_from_descriptions(startDate=startDate, endDate=endDate, order=order)
    mostTags = []
    if limit < 1 or limit >= allPostTags.__len__():
        limit = 10
    for tup in allPostTags.most_common(limit):
        mostTags.append({
            'id': tup[0],
            'label': tup[0],
            'value': tup[1]
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
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type=str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type=str)
    return {
        'data': post_repo.get_position_stats(startDate=startDate, endDate=endDate, order=order)
    }


@app.route("/api/v1/stats/lang")
def langStats():
    order = request.args.get('order', default = 'desc', type=str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type=str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type=str)
    allTags = get_tags_from_descriptions(startDate=startDate, endDate=endDate, order=order)
    langs = ["java", "c#", "python", "javascript", "golang", "dart", "php", "ruby", "c", "c++", "typescript"]
    res = []
    for lang in langs:
        res.append({
            "id": lang,
            "label": lang,
            "value": allTags[lang]
            })
    return {
        'data': sorted(res, key=lambda k: k["value"], reverse=True)
    }


@app.route("/api/v1/stats/tech")
def techStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    allTags = get_tags_from_descriptions(startDate=startDate, endDate=endDate, order=order)
    langs = ["spring", "django", "ruby on rails", "laravel", "express", "flask", ".net", "jsp", "symfony"]
    res = []
    for lang in langs:
        res.append({"tech": lang, "total": allTags[lang]})
    return {
        'data': sorted(res, key=lambda k: k["total"], reverse=True)
    }



@app.route("/api/v1/stats/web")
def wfStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    allTags = get_tags_from_descriptions(startDate=startDate, endDate=endDate, order=order)
    langs = ["spring", "django", "ruby on rails", "laravel", "express", "flask", ".net", "symfony"]
    res = []
    for lang in langs:
        res.append({
            "id": lang,
            "label": lang,
            "value": allTags[lang]
            })
    return {
        'data': sorted(res, key=lambda k: k["value"], reverse=True)
    }



@app.route("/api/v1/stats/frontend")
def fendStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    allTags = get_tags_from_descriptions(startDate=startDate, endDate=endDate, order=order)
    langs = ["reactjs", "vue.js", "jquery", "bootstrap", "angular", "redux", "vuex", "figma", "photoshop"]
    res = []
    for lang in langs:
        res.append({
            "id": lang,
            "label": lang,
            "value": allTags[lang]
            })
    return {
        'data': sorted(res, key=lambda k: k["value"], reverse=True)
    }
