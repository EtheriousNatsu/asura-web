# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: http.py	
@time: 2021/8/17	
"""

import requests


class HttpClient:
    """Send http request"""

    def request(self, url, method, **kwargs):
        """Send a http request.

        Args:
            url(str): Http url.
            data(dict): a dictionary of key-value pairs that
                will be urlencoded and sent as POST data.
            json(dict): a value that will be json encoded
                and sent as POST data if data is not specified.
            params(dict): Query params.
            headers(dict): a dictionary of headers to use
                with the request.

        Returns:
            :obj:`requests.models.Response`
        """
        with requests.Session() as s:
            return s.request(method, url, **kwargs)
