# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: namespace.py	
@time: 2021/8/17	
"""
from .variables import Variables


class Namespace:
    """A database for variables.

    A new instance of this class is created for each test.

    Attributes:
        global_variables(:obj:`core.variables.variables.Variable`):
            store global variables.
        environment_variables(:obj:`core.variables.variables.Variable`):
            store environment variables.
        test_variables(:obj:`core.variables.variables.Variable`):
            store test variables.
        dynamic_variables(:obj:`core.variables.variables.Variable`):
            store setup variables.
    """

    def __init__(self):
        self.global_variables = Variables()
        self.environment_variables = Variables()
        self.test_variables = Variables()
        self.dynamic_variables = Variables()

    def set_global_variable(self, key, value):
        self.global_variables[key] = value

    def set_environment_variable(self, key, value):
        self.environment_variables[key] = value

    def set_test_variable(self, key, value):
        self.test_variables[key] = value

    def set_dynamic_variable(self, key, value):
        self.dynamic_variables[key] = value

    def get_variable_from_environment(self, key):
        return self.environment_variables[key]

    def get_variable_from_global(self, key):
        return self.global_variables[key]

    def replace_scalar(self, item):
        """Replaces variables from a scalar item.

        The Variable precedence is as follows:
            1. Test-level variables (highest precedence)
            2. Dynamic variables using setup steps
            3. Environment variables (lowest precedence)
        """
        result = self.test_variables.replace_scalar(item)
        result = self.dynamic_variables.replace_scalar(result)
        result = self.environment_variables.replace_scalar(result)
        return result
