import requests

def do_query_to_kodilan(number_of_posts):
    kodilan_api_url = f'https://api.kodilan.com/posts?get={number_of_posts}'
    response = requests.get(kodilan_api_url) 

    if response.status_code != 200:
        raise Exception(f'Sayfa basariyla cekilemedi! Status code = {response.status_code}')

    return response.json()

def tagsArrayToStr(tags):
    tagsStr = ""
    for tag in tags:
        tagsStr += tag.get('name') + ','
    if tagsStr.endswith(','):
        tagsStr = tagsStr[:-1]
    return tagsStr

def getPosts():
    response = do_query_to_kodilan(1)
    response = do_query_to_kodilan(response["total"])
    posts = response["data"]
    myPosts = []

    for x in posts:
        slug = x.get('slug')
        position = x.get('position')
        location = x.get('location')
        created_at = x.get('created_at')
        description = x.get('description')
        company = x.get('company').get('name')
        tags = tagsArrayToStr(x.get('tags'))
        myPosts.append({
            "slug": slug,
            "position": position,
            "location": location,
            "created_at": created_at,
            "company": company,
            "description": description,
            "tags": tags
        })

    return myPosts
