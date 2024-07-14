# -*- coding: utf-8 -*-
from fluent.core import Outputer


class UserOutputer(Outputer):
    """用户自定义输出"""

    def handle_item(self, v):
        """处理数据"""
