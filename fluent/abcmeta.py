# -*- coding: utf-8 -*-
"""抽象基类
"""
from abc import ABCMeta, abstractmethod


class ExtensionABC:
    """插件抽象基类"""
    __metaclass__ = ABCMeta

    EXIT_SIGNAL = False
    EXIT_PRE = False

    @abstractmethod
    def start(self):
        """"""

    @abstractmethod
    def exit(self):
        """"""
