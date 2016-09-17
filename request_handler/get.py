from requests import get

from variables import server_url


def get_questions():
    return get('%s/get/questions' % server_url).json()['questions']


def get_question(question_id):
    return get('%s/get/question/%s' % (server_url, question_id)).json()['question']


def get_answers(question_id):
    return get('%s/get/answers/%s' % (server_url, question_id)).json()['answers']


def get_comments(answer_id):
    return get('%s/get/comments/%s' % (server_url, answer_id)).json()['comments']


def get_likes(_id, _type):
    return get('%s/get/likes/%s/%s' % (server_url, _id, _type)).json()['likes']


def get_tags():
    return get('%s/get/tags' % server_url).json()['tags']


def get_notifications(account_id):
    return get('%s/get/notifications/%s' % (server_url, account_id)).json()['notifications']
