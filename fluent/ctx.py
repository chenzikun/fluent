# -*- coding: utf-8 -*-
"""
注册插件用
"""
from functools import wraps

from .scheduler import Scheduler


def register_flow(extension_config_name):
    def decorator(f):
        @wraps(f)
        def inner_func():
            Scheduler.register_flow(extension_config_name, f)

        return inner_func()

    return decorator
