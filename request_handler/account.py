from requests import post

from variables import server_url


def login(user_name, password):
    return post('%s/users/login' % server_url, data={'user_name': user_name, 'password': password}).json()


def register(user_name, password):
    return post('%s/account/sign_up' % server_url, data={'user_name': user_name, 'password': password}).json()
