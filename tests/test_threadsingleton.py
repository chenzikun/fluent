#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2021-04-12   
    Author:       chenzikun         
-------------------------------------------------

"""


from fluent.utils import threadlazyproperty, threadsingleton
from joox_cms.utils import lazy
from joox_cms.lib import singleton

# 替换单线程实例, 因为fluent携带了清理机制
lazy.threadlazyproperty = threadlazyproperty
singleton.singleton = threadsingleton

from joox_cms.lib.log import MyLogger

MyLogger().setlogger('test')

MyLogger().getlogger().warn('adfdafd')