#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2019-11-30
    Author:       chenzikun
-------------------------------------------------

"""
import sys

from fluent.utils import lazyproperty

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


class Compat2(object):
    @lazyproperty
    def quote_plus(self):
        from urllib import quote_plus
        return quote_plus


class Compat3(object):
    @lazyproperty
    def quote_plus(self):
        import urllib.parse.quote_plus as quote_plus
        return quote_plus


if PY2:
    compat = Compat2()
else:
    compat = Compat3()
