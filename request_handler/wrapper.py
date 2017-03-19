from threading import Thread

from requests import request


class RequestWrapper:
    def __init__(self, resps, method, url, headers, data=None, json=None):
        self.method = method
        self.url = url
        self.headers = headers
        self.data = data
        self.json = json
        self.do_in_background = Thread(target=self._make_request, args=[resps])
        self.do_in_background.daemon = True
        self.do_in_background.start()

    def _make_request(self, *args):
        self.resp = request(self.method, self.url, headers=self.headers, data=self.data, json=self.json)
        args[0].put(self.resp.json())  # resps.put(self.resp)
