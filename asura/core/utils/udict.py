# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: udict.py	
@time: 2021/8/17	
"""


def convert_dict_to_list(target_dict):
    """Convert dict to list

        Args:
            target_dict(dict):

        Returns:
            list
    """
    target_list = []

    for k, v in target_dict.items():
        target_list.append({"key": k, "value": v, "enable": True})

    return target_list
