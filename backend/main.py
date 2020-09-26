import flask
import tags_finder
import db
import itertools
import kodilan_client
from collections import Counter
from datetime import date
from flask import request, jsonify
from flask_cors import CORS

app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

tagList = db.get_tags()

@app.route("/api/v1/setupposts")
def setupPosts():
    posts = kodilan_client.getPosts()
    for post in posts:
        db.create_post_record(post)
    return { 'message': 'Success!' }

@app.route("/api/v1/extracttags")
def tag():
    text = request.form.get('text', type = str)
    if (text is None):
        return { 'data': []}
    return { 'data': tags_finder.exportTagsFromText(text, tagList) }

@app.route("/api/v1/stats/tag")
def tagStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    descriptions = db.get_descriptions(startDate=startDate, endDate=endDate, order=order)
    allPostTags = []
    for result in descriptions:
        allPostTags.append(tags_finder.exportTagsFromText(result["description"], tagList))
    allPostTags = itertools.chain.from_iterable(allPostTags) # flat list
    mostTags = []
    for tup in Counter(allPostTags).most_common(50):
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
        'data': db.get_all(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/location")
def locStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': db.get_location_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/company")
def compStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': db.get_company_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/position")
def posStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': db.get_position_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/lang")
def langStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': db.get_lang_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/tech")
def techStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': db.get_web_framework_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/web")
def wfStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': db.get_web_framework_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.route("/api/v1/stats/frontend")
def fendStats():
    order = request.args.get('order', default = 'desc', type = str)
    startDate = request.args.get('startDate', default = date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type = str)
    endDate = request.args.get('endDate', default = date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type = str)
    return {
        'data': db.get_front_end_tech_stats(startDate=startDate, endDate=endDate, order=order)
    }

@app.before_request
def before():
    db.connection = db.get_connection()

@app.after_request
def after(response):
    return response

app.run(host='0.0.0.0')