from requests import get

from variables import server_url


def get_questions():
    return get('%s/get/questions' % server_url)


def get_question(question_id):
    return get('%s/get/question/%s' % (server_url, question_id))


def get_answers(question_id):
    return get('%s/get/answers/%s' % (server_url, question_id))


def get_comments(answer_id):
    return get('%s/get/comments/%s' % (server_url, answer_id))


def get_likes(_id, _type):
    return get('%s/get/likes/%s/%s' % (server_url, _id, _type))


def get_tags():
    return get('%s/get/tags' % server_url)
