from os import path
from base64 import b64encode

from pyDes import triple_des

import request_handler


server_url = 'http://192.168.1.101:8080'
auth_secret_key = 'b5ad2d8123e8809bba576cfa'
auth_message = 'I am authorized'
question_range = 0, 20
PATH_TO_CONF = path.abspath(path.join(path.dirname(request_handler.__file__), '..', 'configuration.json'))
WS_SERVER = "ws://192.168.1.101:8282"


def make_headers(account_id=None, session_id=None):
    return {
        'session': session_id if session_id else '',
        'account': str(account_id) if account_id else None,
        'token': b64encode(bytes(triple_des(auth_secret_key).encrypt(auth_message, padmode=2)))
    }
