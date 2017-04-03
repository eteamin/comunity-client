import json

from kivy.network.urlrequest import UrlRequest

from helpers.variables import server_url, make_headers
from main import on_request_progress, on_post_failure


def login(callback, user_name, password):
    UrlRequest(
        method='post',
        url='{}/users/login'.format(server_url),
        req_headers=make_headers(),
        req_body=json.dumps({"username": user_name, "password": password}),
        on_success=callback,
        on_progress=on_request_progress,
        on_failure=on_post_failure,
        on_error=on_post_failure
    )


def register(callback, user_name, password, email_address):
    UrlRequest(
        method='post',
        url='{}/users/register'.format(server_url),
        req_headers=make_headers(),
        req_body=json.dumps({"username": user_name, "password": password, "email_address": email_address, "bio": ''}),
        on_success=callback,
        on_progress=on_request_progress,
        on_failure=on_post_failure,
        on_error=on_post_failure
    )