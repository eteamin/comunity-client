from requests import post

from variables import server_url


def login(user_name, password):
    return post('%s/account/sign_in' % server_url, data={'user_name': user_name, 'password': password}).json()
