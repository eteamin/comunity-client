from requests import post

from variables import server_url


def login(user_name, password):
    resp = post('%s/users/login' % server_url, json={'username': user_name, 'password': password})
    return resp.json() if resp.status_code == 200 else None


def register(user_name, password):
    return post('%s/account/sign_up' % server_url, data={'username': user_name, 'password': password}).json()
