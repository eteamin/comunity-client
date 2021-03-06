from base64 import b64encode

from pyDes import triple_des


server_url = 'http://192.168.43.150:8080'
image_storage = '{}/storage/images/image-'.format(server_url)
auth_secret_key = 'b5ad2d8123e8809bba576cfa'
auth_message = 'I am authorized'


def make_headers(account_id=None, session_id=None):
    return {
        'session': session_id if session_id else '',
        'account': str(account_id) if account_id else None,
        'token': b64encode(bytes(triple_des(auth_secret_key).encrypt(auth_message, padmode=2))),
    }
