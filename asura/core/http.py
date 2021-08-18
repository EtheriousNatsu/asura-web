# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: http.py	
@time: 2021/8/17	
"""
from urllib import parse

from .utils import (
    HttpClient,
    convert_dict_to_list
)


class HttpExecutor:
    """Http model.

    Args:
        scheme(str): http request protocol.
        host(str): http request host.
        path(str): http request path.
        method(str): http request method.
        namespace(:obj:`core.namespace.Namespace`):
        result():
        headers(:obj:`list` of :obj:`dict`, optional): request headers,
            .e.g.[{'key':1,'value':1, enable:True}].
        params(:obj:`list` of :obj:`dict`, optional): Query params.
        body(str or dict, optional): Request body.
    """

    def __init__(self, scheme, host, path, method, namespace,
                 result, headers=None, params=None, body=None):
        """Initialization
        """

        self.namespace = namespace
        self.result = result
        self._set_scheme(scheme)
        self._set_host(host)
        self._set_path(path)
        self._set_method(method)
        self._set_headers(headers)
        self._set_params(params)
        self._set_body(body)

    def _set_scheme(self, scheme):
        """
        If scheme is None, then use service scheme,
        use scheme otherwise.
        """
        service_scheme = self.namespace.get_variable_from_global('service_scheme')
        self.scheme = scheme if scheme else service_scheme

        self.result.requestScheme = self.scheme

    def _set_host(self, host):
        """
        If host equal to service host, then use
        execution environment's host, use host otherwise.
        """
        service_host = self.namespace.get_variable_from_global('service_host')
        execution_environment_host = self.namespace.get_variable_from_global('execution_environment_host')

        self.host = execution_environment_host if host == service_host else host
        self.host = self.namespace.replace_scalar(self.host)

        self.result.requestHost = self.host

    def _set_path(self, path):
        """Decode http path"""
        self.path = parse.unquote(path)
        self.path = self.namespace.replace_scalar(self.path)

        self.result.requestPath = self.path

    def _set_method(self, method):
        self.method = method

        self.result.requestMethod = self.method

    def _set_headers(self, headers):
        """
        If `namespace` has variable like `{'${name}':'kobe'}`,
        headers like below:
        `[
            {'key': 'C${name}', 'value': 'A${name}', 'enable':True},
            {'key':"kobe", 'value', 'nba', 'enable': False}
        ]`
        then this return's dict will be `{'Ckobe':'Akobe'}`.
        """
        self.headers = {}

        for header_dict in headers:
            if header_dict['enabled']:
                key = self.namespace.replace_scalar(header_dict['key'])
                value = self.namespace.replace_scalar(header_dict['value'])
                self.headers[key] = value

                self.result.requestHeaders.append({
                    'key': key,
                    'value': value,
                    'enabled': True
                })

    def _set_params(self, params):
        """Processing logic like `:method:self._get_headers`
        """
        self.params = {}

        for param_dict in params:
            if param_dict['enabled']:
                key = self.namespace.replace_scalar(param_dict['key'])
                value = self.namespace.replace_scalar(param_dict['value'])
                self.params[key] = value

        self.result.requestQuery = parse.urlencode(
            self.params, quote_via=parse.quote)

    def _set_body(self, body):
        """Return request body.

        Return a body str that already replaced the variable with `namespace`.

        """
        if body is None:
            self.body = None
            return
        elif isinstance(body, dict):
            if self._is_form_encoded_body(body):
                self.body = self._get_urlencode_body(body)
            elif self._is_multipart_form_body(body):
                pass
            elif self._is_raw_body(body):
                self.body = body['data']
        else:
            self.body = body

        self.body = self.namespace.replace_scalar(self.body)
        self.result.requestBody = self.body
        # todo
        self.body = self.body.encode('utf-8')

    def run(self):
        """Send a http request.

        Returns:
            :obj:`requests.models.Response`
        """
        client = HttpClient()

        resp = client.request(
            self._get_url(),
            self.method,
            params=self.params,
            headers=self.headers,
            data=self.body,
            timeout=6
        )

        self._fill_result(resp)

        return resp

    def _fill_result(self, response):
        self.result.responseBody = response.text
        self.result.responseBodySize = len(response.content)
        self.result.responseHeaders = convert_dict_to_list(response.headers)
        self.result.responseStatusCode = response.status_code
        self.result.responseTime = response.elapsed.total_seconds()

    def _get_url(self):
        """Return url.

        First use `urllib.parse.urlunparse` build url.
        if url like `http://www.baidu.com/${x}`, then
        use `namespace.replace_scalar` to replace variable,
        this url will be `http://www.baidu.com/x`.

        Returns:
            str: http url, e.g. `http://www.baidu.com`
        """
        url = parse.urlunparse((
            self.scheme,
            self.host,
            self.path,
            None,
            None,
            None
        ))

        return url

    @staticmethod
    def _is_form_encoded_body(body):
        return body['type'] == 'XWwwFormUrlEncodedBody'

    @staticmethod
    def _is_multipart_form_body(body):
        return body['type'] == 'MultipartFormDataBody'

    @staticmethod
    def _is_raw_body(body):
        return body['type'] == 'RawBody'

    @staticmethod
    def _get_urlencode_body(body):
        """Encode body.

        Use `urllib.parse.urlencode` to build body, and then
        use `urllib.parse.unquote` to decode.

        Process logic:
        `[
            {"key":"${name}","value":10, "enable":True}
        ]`

        => `{"${name}": 10}`

        => `urllib.parse.urlencode`

        => `%24%7Bname%7D=10`

        => `urllib.parse.unquote`

        => `${name}=10`


        Returns:
            str: e.g. name=10&age=100
        """
        big_dict = {}

        for data_dict in body['data']:
            if data_dict['enabled']:
                key = data_dict['key']
                value = data_dict['value']
                big_dict[key] = value

        return parse.unquote(parse.urlencode(big_dict))
