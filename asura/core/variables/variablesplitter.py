# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: variablesplitter.py	
@time: 2021/8/17	
"""
from builtins import ValueError


class VariableSplitter:

    def __init__(self, string, identifiers):
        self.identifier = None
        self.base = None
        self.start = -1
        self.end = -1
        self._identifiers = identifiers
        try:
            self._split(string)
        except ValueError:
            pass
        else:
            self._finalize()

    def get_replaced_base(self):
        return self.base

    def _finalize(self):
        self.identifier = self._variable_chars[0]
        self.base = ''.join(self._variable_chars[2:-1])
        self.end = self.start + len(self._variable_chars)

    def _split(self, string):
        start_index, max_index = self._find_variable(string)
        self.start = start_index
        self._open_curly = 1
        self._state = self._variable_state
        self._variable_chars = [string[start_index], '{']
        self._string = string
        start_index += 2
        for index, char in enumerate(string[start_index:]):
            index += start_index
            try:
                self._state(char)
            except StopIteration:
                return

    def _find_variable(self, string):
        max_end_index = string.rfind('}')
        if max_end_index == -1:
            raise ValueError('No variable end found')
        start_index = self._find_start_index(string, 1, max_end_index)
        if start_index == -1:
            raise ValueError('No variable start found')
        return start_index, max_end_index

    def _find_start_index(self, string, start, end):
        while True:
            index = string.find('{', start, end) - 1
            if index < 0:
                return -1
            if self._start_index_is_ok(string, index):
                return index
            start = index + 2

    def _start_index_is_ok(self, string, index):
        return string[index] in self._identifiers

    def _variable_state(self, char):
        self._variable_chars.append(char)
        if char == '}':
            self._open_curly -= 1
            if self._open_curly == 0:
                raise StopIteration
