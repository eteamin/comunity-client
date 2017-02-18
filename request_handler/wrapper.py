from threading import Thread

from requests import request

from main import retrieve_resp


class RequestWrapper:
    def __init__(self, method, url, headers, data=None, json=None):
        self.method = method
        self.url = url
        self.headers = headers
        self.data = data
        self.json = json
        self.do_in_background = Thread(target=self._make_requests)
        self.do_in_background.daemon = True
        self.do_in_background.start()

    def _make_requests(self):
        self.resp = request(self.method, self.url, headers=self.headers, data=self.data, json=self.json)
        self._callback()

    def _callback(self):
        retrieve_resp(self.resp.json() if self.resp.status_code == 20 else None)


if __name__ == '__main__':
    RequestWrapper(1, 1, 1, 1, 1)
