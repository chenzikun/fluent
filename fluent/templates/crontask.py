#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2021-05-02   
    Author:       chenzikun         
-------------------------------------------------
集成了apsscheluer, 参见
https://apscheduler.readthedocs.io/en/latest/index.html

..example:
from fluent._global import CRON_TASK

..code:
def test():
    pass

CRON_TASK.add_job(test, 'cron', year='*', month='*', day='*', hour='0')
"""


