#!/usr/bin/env
# encoding: utf-8
"""
-------------------------------------------------
    date:          2020-08-08   
    Author:       chenzikun         
-------------------------------------------------
全局变量
"""
from apscheduler.schedulers.background import BackgroundScheduler

SCHEDULER = None

# 保存启动参数--extra
EXTRA = None

# 是否开启了gevent flag
GEVENT = False

# 用户环境变量设置, 避免上报时多个环境的数据混合在一起, telegraf默认会添加host tag
ENV = None

# 服务名, 当前主要是为了区分上报的时候区分单台服务器多进程
WORKER_NAME = None

# apsscheduler实例化的模块，集成的目的一是兼容 gevent, 第二个目的是上报指标
# 不代表实际的Scheduler, 只是为了方便跳转
CRON_TASK = BackgroundScheduler()