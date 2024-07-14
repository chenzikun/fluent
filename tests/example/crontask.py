#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2021-05-02   
    Author:       chenzikun         
-------------------------------------------------

"""
import logging
from fluent.utils import sleep

from fluent._global import CRON_TASK


def test():
    print('add_job test ###################')
    return 'test'


# def test2():
#     raise KeyError


# CRON_TASK.add_job(test, 'interval', seconds=1)

