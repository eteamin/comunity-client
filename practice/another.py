import time
import requests


for i in range(3, 2500):
    a= requests.post('http://192.168.1.101:8080/posts', json={
        'post_type': 'Question',
        'account_id': 2,
        'description': i,
        'title': i,
        'tags': 'hello',
        'parent_id': None
    })
    print a.json()