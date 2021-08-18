# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: results.py	
@time: 2021/8/17	
"""


class _BaseSetupResult:
    type = None

    def __init__(self, step_id):
        self.id = step_id
        self.log = []

    def add_log(self, key=None, value=None, log=None):
        if log:
            msg = log
        else:
            msg = '%s: %s' % (key, value)

        self.log.append(
            {"msg": msg}
        )

    def serializer(self):
        return {
            'id': self.id,
            'log': self.log,
            'type': self.type
        }


class RandomSetupResult(_BaseSetupResult):
    type = 'RandomSetupResult'


class HttpReqSetupResult(_BaseSetupResult):
    type = 'HttpReqSetupResult'

    def __init__(self, step_id):
        super().__init__(step_id)
        self.http_result = HttpReqResult()

    def serializer(self):
        """"""
        local_serializer = super().serializer()
        http_serializer = self.http_result.serializer()

        return {**local_serializer, **http_serializer}


class HttpReqTeardownResult(HttpReqSetupResult):
    type = 'HttpReqTeardownResult'


class HttpReqResult:
    def __init__(self):
        self.requestBody = None
        self.requestScheme = None
        self.requestHeaders = []
        self.requestHost = None
        self.requestMethod = None
        self.requestPath = None
        self.requestQuery = None
        self.responseBody = None
        self.responseBodySize = None
        self.responseHeaders = []
        self.responseStatusCode = None
        self.responseTime = None

    def serializer(self):
        return {
            'requestBody': self.requestBody,
            'requestScheme': self.requestScheme,
            'requestHeaders': self.requestHeaders,
            'requestHost': self.requestHost,
            'requestMethod': self.requestMethod,
            'requestPath': self.requestPath,
            'requestQuery': self.requestQuery,
            'responseBody': self.responseBody,
            'responseBodySize': self.responseBodySize,
            'responseHeaders': self.responseHeaders,
            'responseStatusCode': self.responseStatusCode,
            'responseTime': self.responseTime
        }
