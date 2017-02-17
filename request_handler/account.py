from requests import post

from variables import server_url, make_headers


def login(user_name, password):
    resp = post(
        '%s/users/login' % server_url,
        json={'username': user_name, 'password': password},
        headers=make_headers()
    )
    return resp.json() if resp.status_code == 200 else None


def register(user_name, password, email_address):
    data = {
        'username': user_name,
        'password': password,
        'email_address': email_address,
        'bio': None
    }
    resp = post('%s/users/register' % server_url, data=data)
    return resp.json() if resp.status_code == 200 else None
