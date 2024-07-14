#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2021-04-09   
    Author:       chenzikun         
-------------------------------------------------

"""
from fluent.utils import sleep


class InternalMixin:
    interval_second = 0
    interval_chunks = []
    EXIT_SIGNAL = None

    def rerange_interval_chunks(self):
        INTERVAL_CHUNK = 5
        if self.interval_second <= INTERVAL_CHUNK:
            chunks = [self.interval_second]
        else:
            chunks = [INTERVAL_CHUNK] * int(self.interval_second / INTERVAL_CHUNK)
            if self.interval_second % INTERVAL_CHUNK > 0:
                chunks.append(self.interval_second % INTERVAL_CHUNK)
        return chunks

    def _interval(self):
        """监控的频率"""
        for chunk in self.interval_chunks:
            if not self.EXIT_SIGNAL:
                sleep(chunk)