# -*- coding: utf-8 -*-
"""
信号
"""
import uuid


class JobExit:
    """"""


class FluentSignal:
    """非内存队列, 无法使用类信号"""
    QueueStopBlockedSignal = 'JobExit:salt:' + uuid.uuid4().hex
