from functools import partial

from kivy.network.urlrequest import UrlRequest

from helpers.variables import server_url, make_headers
from main import on_request_progress, on_get_failure


def get_questions(callback, id, session, _from, to, screen):
    UrlRequest(
        method='get',
        url='{}/posts/get_questions?from={}&to={}'.format(server_url, _from, to),
        req_headers=make_headers(session_id=session, account_id=id),
        on_success=callback,
        on_progress=on_request_progress,
        on_error=partial(on_get_failure, screen),
        on_failure=partial(on_get_failure, screen)
    )


def get_question(callback, question_id, account_id, session, screen):
    UrlRequest(
        method='get',
        url='{}/posts/{}'.format(server_url, question_id),
        req_headers=make_headers(session_id=session, account_id=account_id),
        on_success=callback,
        on_progress=on_request_progress,
        on_error=partial(on_get_failure, screen),
        on_failure=partial(on_get_failure, screen)
    )


def get_children(resps, parent_id, account_id, session):
    RequestWrapper(
        resps,
        'get',
        '%s/posts/get_children/%s' % (server_url, parent_id),
        headers=make_headers(session_id=session, account_id=account_id),
    )


def get_ranking(callback, account_id, session, _from, to):
    UrlRequest(
        method='get',
        url='{}/ranking?_from={}&to={}'.format(server_url, _from, to),
        req_headers=make_headers(session_id=session, account_id=account_id),
        on_success=callback,
        on_progress=on_request_progress,
    )


def get_total_accounts(callback, account_id, session):
    UrlRequest(
        method='get',
        url='{}/accounts/total'.format(server_url),
        req_headers=make_headers(session_id=session, account_id=account_id),
        on_success=callback,
        on_progress=on_request_progress
    )


def get_about_us(callback, account_id, session, screen):
    UrlRequest(
        method='get',
        url='{}/about_us'.format(server_url),
        req_headers=make_headers(session_id=session, account_id=account_id),
        on_success=callback,
        on_progress=on_request_progress,
        on_error=partial(on_get_failure, screen),
        on_failure=partial(on_get_failure, screen)
    )


def get_notifications(account_id):
    return get('%s/get/notifications/%s' % (server_url, account_id), headers=make_headers()).json()['notifications']


def get_tags():
    return get('%s/tags' % server_url, headers=make_headers()).json()['tags']


def get_user(user_id):
    resp = get('%s/accounts/%s' % (server_url, user_id), headers=make_headers())
    return resp.json()['account'] if resp.status_code == 200 else None


def get_image(account_id):
    image = get('%s/get/image/%s' % (server_url, account_id), headers=make_headers())
    with open('%s/%s.jpg' % (files_path, account_id), 'w') as user_image:
        user_image.write(image.content)
