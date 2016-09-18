from requests import post

from variables import server_url


def post_question(title, content, account_id, tag):
    params = {
        'title': title,
        'content': content,
        'account_id': account_id,
        'tag': tag
    }
    post('%s/post/question' % server_url, data=params)


def post_answer(content, account_id, question_id):
    params = {
        'content': content,
        'account_id': account_id,
        'question_id': question_id
    }
    post('%s/post/answer' % server_url, data=params)


def post_comment(content, account_id, answer_id):
    params = {
        'content': content,
        'account_id': account_id,
        'answer_id': answer_id
    }
    post('%s/post/answer' % server_url, data=params)


def post_like(account_id, question_id=None, answer_id=None):
    params = {
        'account_id': account_id
    }
    if question_id:
        params['question_id'] = question_id
    else:
        params['answer_id'] = answer_id
    post('%s/post/like' % server_url, data=params)


def post_image(account_id, image_path):
    with open(image_path, 'rb') as image_file:
        params = {
            'account_id': account_id,
        }
        post('%s/post/image' % server_url, data=params, files=dict(image=image_file.read()))
