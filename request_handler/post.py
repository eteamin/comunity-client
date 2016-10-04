from requests import post

from variables import server_url


def post_question(title, content, account_id, tags):
    params = {
        'title': title,
        'content': content,
        'account_id': account_id,
        'tags': tags
    }
    return post('%s/post/question' % server_url, data=params).json()


def post_answer(content, account_id, question_id):
    params = {
        'content': content,
        'account_id': account_id,
        'question_id': question_id
    }
    return post('%s/post/answer' % server_url, data=params).json()


def post_comment(content, account_id, answer_id):
    params = {
        'content': content,
        'account_id': account_id,
        'answer_id': answer_id
    }
    return post('%s/post/answer' % server_url, data=params).json()


def post_like(account_id, question_id=None, answer_id=None):
    params = {
        'account_id': account_id
    }
    if question_id:
        params['question_id'] = question_id
    else:
        params['answer_id'] = answer_id
    return post('%s/post/like' % server_url, data=params).json()


def post_image(account_id, image_path):
    with open(image_path, 'rb') as image_file:
        params = {
            'account_id': account_id,
        }
        return post('%s/post/image' % server_url, data=params, files=dict(image=image_file.read())).json()
