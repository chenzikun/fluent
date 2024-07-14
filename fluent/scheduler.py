# -*- coding: utf-8 -*-
"""调度器

* 负责线程调度和input, processor, output管理
* 保证线程安全执行

Todo:
    是否考虑consumer, shuffle, producer在不同的进程中

"""
import logging
import signal
import sys
import threading

import gevent.signal

from fluent import _global
from .utils import threadlazyproperty

from .core.utils import PY2
from .model import Config, PersistQueue, MemQueue
from .reporter import Telegraf


class Scheduler:
    """常驻进程或定时任务

    不在同一个进程应在外部实现，不改变同一个进程内部逻辑

    Args:
        config: 配置
        input(Inputer): job.input
        processor(Processor): job.Processor
        output(Outputer): job.Outputer
        job_dir: job所在路径

    Attributes:
        conf: 配置文件
        e: Event， 阻塞主线程
        core_flows: 数据处理流程, 按照input-> process -> output做排序
    """

    _global_config = None
    SETUP_ASIDE_FLOWS = {}

    def __init__(self, config, input, processor, output, task_name=None):
        logging.debug('init Scheduler')
        self._global_config = config
        self.conf = Config(config, 'scheduler')
        config['__task_name'] = self.conf.get('task_name') if self.conf.get('task_name') else task_name
        self._task_name = task_name
        self.input = input(self, Config(config, 'input'))
        self.processor = processor(self, Config(config, 'process'))
        self.output = output(self, Config(config, 'output'))
        if self.conf.get('persist_queue'):
            self.q_of_inputer_processor = PersistQueue(path=self.conf.get('input_q_path'),
                                                       maxsize=self.conf.get("input_q_size"))
            self.q_of_processor_outputer = PersistQueue(path=self.conf.get('output_q_path'),
                                                        maxsize=self.conf.get("output_q_size"))
        else:
            self.q_of_inputer_processor = MemQueue(maxsize=self.conf.get("input_q_size"))
            self.q_of_processor_outputer = MemQueue(maxsize=self.conf.get("output_q_size"))
        self.core_flows = [self.input, self.processor, self.output]
        self.aside_flows = {}
        self.init_aside_flows()
        self.e = threading.Event()

    @threadlazyproperty
    def reporter(self):
        report_conf = self.conf.get('reporter')
        return Telegraf(report_conf, self._task_name)

    def init_aside_flows(self):
        for flow_name, flow in self.SETUP_ASIDE_FLOWS.items():
            config = self._global_config.get(flow_name)
            if config:
                self.aside_flows[flow_name] = flow(self, config)

    @classmethod
    def register_flow(cls, extension_name, flow):
        """注册流程"""
        cls.SETUP_ASIDE_FLOWS[extension_name] = flow

    def _start_flow(self, flow_name, flow):
        if _global.GEVENT:
            from fluent._gevent import start_one_thread as _start_one_thread
            _start_one_thread(flow.start, flow_name)
        else:
            t = threading.Thread(target=flow.start)
            t.daemon = True
            t.setName(flow_name)
            t.start()

    def start_flows_on_threads(self):
        """多线程启动flows"""
        for flow_name, flow in self.aside_flows.items():
            self._start_flow(flow_name, flow)
            logging.info("start {}".format(flow_name))
        self.input.start_threads()
        self.processor.start_threads()
        self.output.start_threads()

    def _daemon(self):
        """阻塞主线程"""
        self.e.wait()

    def set_signal(self):
        """接管信号"""
        if _global.GEVENT:
            gevent.signal_handler(signal.SIGTERM, self.exit)
            gevent.signal_handler(signal.SIGINT, self.exit)
        else:
            signal.signal(signal.SIGINT, self.exit)
            signal.signal(signal.SIGTERM, self.exit)
            if PY2:
                signal.pause()

    def start(self):
        """启动Scheduler， 并接管Ctrl+c和 kill -2(TERM) 中断信号"""
        logging.info("\n{}\n".format(self.conf.get("signature"), "\n ==== fluent start! ====\n"))
        self.start_flows_on_threads()
        self.set_signal()
        self._daemon()
        # wait to child thread signal to stop
        self.stop()
        sys.exit(0)

    def stop_aside_flows(self, pre_tag):
        """停止插件"""
        for _, flow in self.aside_flows.items():
            if flow.EXIT_PRE == pre_tag:
                logging.info("{}: Prepared to quit".format(flow.__class__.__name__))
                flow.exit()
                logging.info("{}: Finished to quit".format(flow.__class__.__name__))

    def stop(self, signalnum=None):
        logging.warning("received signal of quit! signalnum => {}".format(str(signalnum)))
        #: 获取等待状态
        self.stop_aside_flows(True)
        for cf in self.core_flows:
            logging.info("{}: Prepared to quit".format(cf))
            cf.exit()
            logging.info("{}: Finished to quit".format(cf))
        self.stop_aside_flows(False)
        logging.info("quit!")

    def exit(self, signalnum=None, handler=None):
        """处理完当前的数据后关闭

        在这里给各个线程发送信号，且按顺序关闭设置信号
        """

        # else:
        self.stop(signalnum)
        self.e.set()
        sys.exit(0)
