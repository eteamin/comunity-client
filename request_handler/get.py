from requests import get

from variables import server_url, files_path, question_range


def get_questions():
    resp = get('%s/posts/get_questions' % server_url, json={'from': question_range[0], 'to': question_range[1]})
    return resp.json()['questions'] if resp.status_code == 200 else []


def get_question(question_id, account_id):
    resp = get('%s/posts/%s' % (server_url, question_id))
    return resp.json()['post'] if resp.status_code == 200 else None


def get_children(parent_id):
    resp = get('%s/posts/get_children/%s' % (server_url, parent_id))
    return resp.json()['children'] if resp.status_code == 200 else []


def get_notifications(account_id):
    return get('%s/get/notifications/%s' % (server_url, account_id)).json()['notifications']


def get_tags():
    return get('%s/tags' % server_url).json()['tags']


def get_user(user_id):
    resp = get('%s/accounts/%s' % (server_url, user_id))
    return resp.json()['account'] if resp.status_code == 200 else None


def get_image(account_id):
    image = get('%s/get/image/%s' % (server_url, account_id))
    with open('%s/%s.jpg' % (files_path, account_id), 'w') as user_image:
        user_image.write(image.content)
