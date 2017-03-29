from requests import get

from request_handler.wrapper import RequestWrapper
from helpers.variables import server_url, question_range, make_headers


def get_questions(resps, id, session):
    RequestWrapper(
        resps,
        'post',
        '%s/posts/get_questions' % server_url,
        headers=make_headers(session_id=session, account_id=id),
        data={'from': question_range[0], 'to': question_range[1]},
    )


def get_question(resps, question_id, account_id, session):
    RequestWrapper(
        resps,
        'get',
        '%s/posts/%s' % (server_url, question_id),
        headers=make_headers(session_id=session, account_id=account_id),
    )


def get_children(resps, parent_id, account_id, session):
    RequestWrapper(
        resps,
        'get',
        '%s/posts/get_children/%s' % (server_url, parent_id),
        headers=make_headers(session_id=session, account_id=account_id),
    )


def get_ranking(resps, account_id, session, _from, to):
    RequestWrapper(
        resps,
        'get',
        '{}/ranking?_from={}&to={}'.format(server_url, _from, to),
        headers=make_headers(session_id=session, account_id=account_id),
    )


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
