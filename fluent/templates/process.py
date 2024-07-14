# -*- coding: utf-8 -*-
from fluent.core import Processor


class UserProcessor(Processor):
    """用户自定义处理流程"""

    def handle_item(self, v):
        """处理数据"""
