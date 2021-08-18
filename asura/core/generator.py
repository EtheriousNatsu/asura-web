# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: generator.py	
@time: 2021/8/17	
"""
from .http import HttpExecutor
from .utils import (
    generator_random_number,
    generator_random_str,
    generator_random_timestamp,
    generator_random_uuid
)


class _BaseGenerator:
    """Generator base class.

    Args:
        settings(dict): Configuration information.

    Attributes:
        _settings(dict): Configuration information.
    """

    def __init__(self, settings):
        """Initialization.
        """
        self._settings = settings

    def generate(self, namespace, result):
        """Abstract method
        """
        raise NotImplementedError

    @property
    def settings(self):
        """Return settings.
        """
        return self._settings


class RandomGenerator(_BaseGenerator):
    """Generate a random data.
    """

    def generate(self, namespace, result):
        """Generate a random data.

        Args:
            namespace(:obj:`core.namespace.Namespace`): execution environment.
            result():
        Returns:
            generator object
        """
        while 1:
            yield {
                'IntVar': generator_random_number(),
                'TextVar': generator_random_str(),
                'TimestampVar': generator_random_timestamp(),
                'UuidVar': generator_random_uuid()
            }


class HttpReqGenerator(_BaseGenerator):
    """Send a http request.
    """

    def generate(self, namespace, result):
        """Use :class:`core.http.HttpExecutor` instance to generate data.

        Args:
            namespace(:obj:`core.namespace.Namespace`): execution environment.
            result():
        """
        http = HttpExecutor(
            self.settings['requestScheme'],
            self.settings['requestHost'],
            self.settings['requestPath'],
            self.settings['requestMethod'],
            namespace,
            result.http_result,
            headers=self.settings['requestHeaders'],
            params=self.settings['requestQuery'],
            body=self.settings['requestBody']
        )

        return http.run()
