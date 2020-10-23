import itertools
from datetime import date
from flask import request, Blueprint, g, session
from app import app
from collections import Counter
from app.repo import post_repo
from app.business import tags_finder
from app.interfaces import kodilan_client
from app.utils import html_utils
import re

stats_api = Blueprint('stats', __name__, url_prefix="/api/v1")
tagsList = list = []


@app.before_first_request
def t():
    global tagsList
    tagsList = post_repo.get_tags()


@stats_api.route("/setupposts")
def setupPosts():
    posts = kodilan_client.get_posts()
    for post in posts:
        print('here')
        post_repo.create_post_record(post)
    return {'message': 'Success!'}


@stats_api.route("/extracttags", methods=["GET", "POST"])
def tag():
    text = request.form.get('text', type=str)
    if (html_utils.check_is_it_url(text)):
        html = html_utils.get_page_content(text)
        text = html_utils.parse_job_description_from_html(html)
    if (text is None):
        return {'data': []}
    return {'data': tags_finder.export_tags_from_text(text, tagsList)}


def get_tags_from_descriptions(startDate, endDate, order):
    descriptions = post_repo.get_descriptions_and_tags(startDate=startDate, endDate=endDate, order=order)
    allPostTags = []
    for result in descriptions:
        postContent = result["description"] + "\n" + result["tags"]
        allPostTags.append(tags_finder.export_tags_from_text(postContent, tagsList))
    counter = Counter(itertools.chain.from_iterable(allPostTags)) # flat list
    return counter


def get_tags_from_positions(startDate, endDate, order):
    descriptions = post_repo.get_positions(startDate=startDate, endDate=endDate, order=order)
    allPostTags = []
    for result in descriptions:
        postContent = result["position"]
        allPostTags.append(tags_finder.export_tags_from_text(postContent, tagsList))
    counter = Counter(itertools.chain.from_iterable(allPostTags)) # flat list
    return counter


def get_first_nth_tags_from_descriptions_count(nth, startDate, endDate, order):
    descriptions = post_repo.get_descriptions(startDate=startDate, endDate=endDate, order=order)
    allPostTags = []
    for result in descriptions:
        allPostTags.append(tags_finder.export_tags_from_text(result["description"], tagsList)[:3])

    c = Counter(itertools.chain.from_iterable(allPostTags))

    with open('tags.csv', 'w') as writer:
        data_str = ''
        for pt in c.most_common():
            data_str += f'{pt[0]},{pt[1]}\r\n'
        writer.write(data_str)
    return allPostTags


def get_first_nth_tags_from_descriptions(nth, startDate, endDate, order):
    descriptions = post_repo.get_descriptions(startDate=startDate, endDate=endDate, order=order)
    allPostTags = []
    for result in descriptions:
        postContent = result["description"]
        allPostTags.append({
                'position': result['position'],
                'tags': ",".join(tags_finder.export_tags_from_text(postContent, tagsList)[:3])
            }
        )

    with open('tags.csv', 'w') as writer:
        data_str = ''
        for pt in allPostTags:
            data_str += f'{pt["position"]},{pt["tags"]}\r\n'
        writer.write(data_str)
    return allPostTags


def get_posts_that_have_tag(tag):
    order = request.args.get('order', default='desc', type=str)
    startDate = request.args.get('startDate', default=date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type=str)
    endDate = request.args.get('endDate', default=date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type=str)
    descriptions = post_repo.get_descriptions(startDate=startDate, endDate=endDate, order=order)
    posts = []
    excepts = ['css3|css', 'git', 'english|ingilizce|i̇ngilizce', 'html5|html']
    for result in descriptions:
        postContent = result["description"]
        if len(tags_finder.export_tags_from_text(postContent, [tag])) > 0:
            relateds = tags_finder.export_tags_from_text(postContent, tagsList, excepts + [tag])
            posts.extend(relateds)
    tags = {}
    #for tag in Counter(posts).most_common(20):
    #    tags[f'{tag[0]}'] = tag[1]
    return Counter(posts).most_common()


@app.route("/api/v1/stats/tag")
def tagStats():
    order = request.args.get('order', default='desc', type=str)
    startDate = request.args.get('startDate', default=date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type=str)
    endDate = request.args.get('endDate', default=date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type=str)
    limit = request.args.get('limit', default=15, type=int)
    allPostTags = get_tags_from_positions(startDate=startDate, endDate=endDate, order=order)
    mostTags = []
    if limit < 1 or limit >= allPostTags.__len__():
        limit = allPostTags.__len__()
    index = 0
    for tup in allPostTags.most_common():
        mostTags.append({
            'label': tup[0],
            'value': tup[1],
            'relateds': get_posts_that_have_tag(tup[0])
        })
        index += 1
    csv = dictToCsvWithRelateds(mostTags)
    with open('tags.csv', 'w') as writer:
        writer.write(csv)

    return {
        'data': mostTags
    }

@app.route("/api/v1/stats/f3")
def tagStatsF3():
    order = request.args.get('order', default='desc', type=str)
    startDate = request.args.get('startDate', default=date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type=str)
    endDate = request.args.get('endDate', default=date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type=str)
    limit = request.args.get('limit', default=15, type=int)
    allPostTags = get_first_nth_tags_from_descriptions(3,startDate=startDate, endDate=endDate, order=order)
    return {'data': allPostTags}


@app.route("/api/v1/stats/f32")
def tagStatsF32():
    order = request.args.get('order', default='desc', type=str)
    startDate = request.args.get('startDate', default=date(date.today().year, 1, 1).strftime("%Y-%m-%d"), type=str)
    endDate = request.args.get('endDate', default=date(date.today().year, 12, 31).strftime("%Y-%m-%d"), type=str)
    limit = request.args.get('limit', default=15, type=int)
    allPostTags = get_first_nth_tags_from_descriptions_count(3,startDate=startDate, endDate=endDate, order=order)
    return {'data': allPostTags}


def dictToCsv(datas) -> str:
    data_str = ''
    for data in datas:
        data_str += f'{data["label"]}:{data["value"]}\r\n'
    return data_str


def dictToCsvWithRelateds(datas) -> str:
    data_str = ''
    for data in datas:
        rels = ''
        for d in data['relateds']:
            rels += f'{d[0]}({d[1]}),'
        data_str += f'{data["label"]}({data["value"]}), {rels}\r\n'
    return data_str
