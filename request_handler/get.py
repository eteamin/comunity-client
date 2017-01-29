from requests import get

from variables import server_url, files_path, question_range


def get_questions():
    resp = get('%s/posts/get_questions' % server_url, json={'from': question_range[0], 'to': question_range[1]}).json()
    return resp['questions'] if resp else []


def get_question(question_id, account_id):
    return get('%s/posts/%s' % (server_url, question_id)).json()['post']


def get_answers(question_id):
    return get('%s/posts/get_answers/%s' % (server_url, question_id)).json()['answers']


def get_comments(answer_id):
    return get('%s/comments/%s' % (server_url, answer_id)).json()['comments']


def get_likes(_id, _type):
    return get('%s/likes/%s/%s' % (server_url, _id, _type)).json()['likes']


def get_tags():
    return get('%s/tags' % server_url).json()['tags']


def get_notifications(account_id):
    return get('%s/get/notifications/%s' % (server_url, account_id)).json()['notifications']


def get_image(account_id):
    image = get('%s/get/image/%s' % (server_url, account_id))
    with open('%s/%s.jpg' % (files_path, account_id), 'w') as user_image:
        user_image.write(image.content)
