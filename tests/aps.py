#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2021-05-02   
    Author:       chenzikun         
-------------------------------------------------

"""
from joox_cms.lib.log import set_info_console_log
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler({
    # 'apscheduler.jobstores.mongo': {
    #      'type': 'mongodb'
    # },
    # 'apscheduler.jobstores.default': {
    #     'type': 'sqlalchemy',
    #     'url': 'sqlite:///jobs.sqlite'
    # },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    # 'apscheduler.executors.processpool': {
    #     'type': 'processpool',
    #     'max_workers': '5'
    # },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': 'UTC',
})

set_info_console_log()
def test():
    print('test')

scheduler.add_job(test, 'interval', seconds=5)
scheduler.start()