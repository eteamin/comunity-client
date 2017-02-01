from os import path
from base64 import b64encode

from pyDes import triple_des


server_url = 'http://localhost:8080'
files_path = path.abspath(path.join(path.dirname(__file__), 'files'))
auth_secret_key = 'b5ad2d8123e8809bba576cfa'
auth_message = 'I am authorized'
question_range = 0, 20


def make_headers(account_id=None):
    return {
        'account': str(account_id) if account_id else None,
        'token': b64encode(bytes(triple_des(auth_secret_key).encrypt(auth_message, padmode=2)))
    }
