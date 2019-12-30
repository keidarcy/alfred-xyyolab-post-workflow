# encoding: utf-8

import sys
from workflow import Workflow, ICON_WEB, web


def get_posts():
    url = 'https://www.xyyolab.com/api/posts'
    params = dict(format='json')
    r = web.get(url, params)

    r.raise_for_status()

    result = r.json()
    posts = result
    return posts


# query = 'Laravel'

# posts = [post for post in get_posts() if query in post['title']]

# print(posts[1]['title'])
def search_key_for_post(post):
    elements = []
    elements.append(post['title'])
    elements.append(post['summary'])
    # elements.append(post['body'])
    return u' '.join(elements)


def main(wf):

    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    # Retrieve posts from cache if available and no more than 600
    # seconds old
    posts = wf.cached_data('posts', get_posts, max_age=600)

    # If script was passed a query, use it to filter posts
    if query:
        posts = [post for post in posts if query in post['title']]
    #posts = wf.filter(query, posts, key=search_key_for_post)

    for post in posts:
        wf.add_item(title=post['title'],
                    subtitle=post['summary'],
                    arg='https://www.xyyolab.com/show/'+post['slug'],
                    valid=True,
                    icon=ICON_WEB)

    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    sys.exit(wf.run(main))
