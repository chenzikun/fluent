# -*- coding: utf-8 -*-
"""
定义异常
"""


class ConfigNotFound(Exception):
    """配置没有写入时抛出异常"""


class NotSupportException(Exception):
    """配置支持时抛出异常"""
