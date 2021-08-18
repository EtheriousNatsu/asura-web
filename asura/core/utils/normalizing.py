# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: normalizing.py	
@time: 2021/8/17	
"""

import re
from collections import UserDict

_WHITESPACE_REGEXP = re.compile('\s+')


def normalize(string, ignore=list(), lower_case=True, spaceless=True):
    if spaceless:
        string = _WHITESPACE_REGEXP.sub('', string)
    if lower_case:
        string = string.lower()
        ignore = [i.lower() for i in ignore]
    for ign in ignore:
        string = string.replace(ign, '')
    return string


class NormalizedDict(UserDict):
    """Custom dictionary implementation automatically normalizing keys."""

    def __init__(self,
                 initial=None,
                 ignore=list(),
                 lower_case=True,
                 spaceless=True):
        super().__init__()
        self._keys = {}
        self._normalize = lambda s: normalize(s, ignore, lower_case, spaceless)
        if initial:
            self._add_initial(initial)

    def _add_initial(self, items):
        if hasattr(items, 'items'):
            items = items.items()
        for key, value in items:
            self[key] = value

    def update(self, dictionary=None, **kwargs):
        if dictionary:
            UserDict.update(self, dict)
            for key in dictionary:
                self._add_key(key)
        if kwargs:
            self.update(kwargs)

    def _add_key(self, key):
        normalize_key = self._normalize(key)
        self._keys.setdefault(normalize_key, key)
        return normalize_key

    def set(self, key, value):
        normalize_key = self._add_key(key)
        self.data[normalize_key] = value

    __setitem__ = set

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def __getitem__(self, key):
        return self.data[self._normalize(key)]

    def pop(self, key):
        normalize_key = self._normalize(key)
        del self._keys[normalize_key]
        return self.data.pop(normalize_key)

    __delitem__ = pop

    def has_key(self, key):
        return self._normalize(key) in self.data

    __contains__ = has_key

    def keys(self):
        return [self._keys[normalize_key]
                for normalize_key in sorted(self._keys)]

    def __iter__(self):
        return iter(self.keys())

    def values(self):
        return [self[key] for key in self]

    def items(self):
        return [(key, self[key]) for key in self]

    def copy(self):
        copy = UserDict.copy(self)
        copy._keys = self._keys.copy()
        return copy

    def __str__(self):
        return str(dict(self.items()))
