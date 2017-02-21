from requests import get

from request_handler.wrapper import RequestWrapper
from variables import server_url, question_range, make_headers


def get_questions(resps, me):
    RequestWrapper(
        resps,
        'post',
        '%s/posts/get_questions' % server_url,
        headers=make_headers(session_id=me['session'], account_id=me['id']),
        data={'from': question_range[0], 'to': question_range[1]},
    )


def get_question(question_id, account_id):
    resp = get('%s/posts/%s' % (server_url, question_id), headers=make_headers(account_id))
    return resp.json()['post'] if resp.status_code == 200 else None


def get_children(parent_id):
    resp = get('%s/posts/get_children/%s' % (server_url, parent_id), headers=make_headers())
    return resp.json()['children'] if resp.status_code == 200 else []


def get_notifications(account_id):
    return get('%s/get/notifications/%s' % (server_url, account_id), headers=make_headers()).json()['notifications']


def get_tags():
    return get('%s/tags' % server_url, headers=make_headers()).json()['tags']


def get_user(user_id):
    resp = get('%s/accounts/%s' % (server_url, user_id), headers=make_headers())
    return resp.json()['account'] if resp.status_code == 200 else None

#
# def get_image(account_id):
#     image = get('%s/get/image/%s' % (server_url, account_id), headers=make_headers())
#     with open('%s/%s.jpg' % (files_path, account_id), 'w') as user_image:
#         user_image.write(image.content)
