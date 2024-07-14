# -*- coding: utf-8 -*-
import logging
import time

from fluent.core import Outputer


class UserOutputer(Outputer):
    """用户自定义输出"""

    def handle_item(self, v):
        """处理数据"""
        logging.info(v)
        # print("UserOutputer: gevent monkey patch has occurred")
        return v + v
