from variables import server_url, make_headers

from wrapper import RequestWrapper


def login(resps, user_name, password):
    RequestWrapper(
        resps,
        'post',
        '%s/users/login' % server_url,
        json={'username': user_name, 'password': password},
        headers=make_headers()
    )


def register(resps, user_name, password, email_address):
    payload = {
        'username': user_name,
        'password': password,
        'email_address': email_address,
        'bio': None
    }
    RequestWrapper(resps, 'post', '%s/users/register' % server_url, json=payload, headers=make_headers())
