# -*- coding: utf-8 -*-
import logging

import gevent.socket
from fluent.core import Inputer
from fluent.utils import sleep
import socket

class UserInputer(Inputer):
    """用户定义handle_item"""

    def __init__(self, s, conf):
        super(UserInputer, self).__init__(s, conf)
        self.count = 0

    def handle_item(self):
        """"""
        self.count += 1
        # sleep(1)
        if self.count % 500 == 0:
            logging.info(self.count)

        # if socket.socket is gevent.socket.socket:
        #     print("input: gevent monkey patch has occurred")
        return self.count
