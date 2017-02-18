from variables import server_url, make_headers

from wrapper import RequestWrapper


def login(user_name, password):
    RequestWrapper(
        'post',
        '%s/users/login' % server_url,
        json={'username': user_name, 'password': password},
        headers=make_headers()
    )


def register(user_name, password, email_address):
    payload = {
        'username': user_name,
        'password': password,
        'email_address': email_address,
        'bio': None
    }
    RequestWrapper('post', '%s/users/register' % server_url, json=payload, headers=make_headers())
