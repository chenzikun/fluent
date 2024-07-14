.. _config:

config文件的使用方式
====================

一些关键配置的含义解释

.. code-block:: yaml

    # 是否开启gevent, 使用gevent可以获得更高的IO效率和更小的资源使用
    gevent: true

    # 日志:
    logging:
        # 当不想使用fluent的日志系统时，关闭这个选项，default = true
        fluent_log: true

    scheduler:
        # 管道缓存大小
        input_q_size: 100
        output_q_size: 100

        # 是否开启influxdb上报，默认使用telegraf做代理
        reporter:

    input:
        # 线程数
        threads: 1
        # input函数是否循环，当你的数据源是一次性函数调用，将loop置为false
        loop: true

    monitor:
        # 上报间隔，包括耗时，TPS等
        interval: 60
        measurement: fluent_queue

    # 动态线程配置
    thread_flex：

    # 资源监控，包含CPU和MEM
    monitor_resource: