# -*- coding: utf-8 -*-
"""命令行

1. 参数管理
2. job模块加载

"""
import logging
import os
import shutil
import sys

import click
import yaml

from fluent.core.utils import import_by_abspath
from fluent.model import Extra
from . import _global
from .log import set_logger


def get_conf(filepath):
    """加载配置文件

    Args:
        filepath:

    Returns:
        dict: conf配置文件
    """
    with open(filepath) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def extract_worker_dir(directory):
    """解析worker文件夹

    Args:
        directory (str): 工作目录文件夹

    Returns:
        tuple: a list of Producer, shuffler, Consumer

    """
    from .core.utils import import_module

    # 将当前工作空间加入到sys.path
    pwd = os.getcwd()
    sys.path.append(pwd)
    from .core import Inputer, Processor, Outputer
    if os.path.exists(os.path.join(directory, '__init__.py')):
        import_by_abspath('init', os.path.join(directory, '__init__.py'))
    inputer = import_module(directory, "input.py", Inputer)
    processor = import_module(directory, "process.py", Processor)
    outputer = import_module(directory, "output.py", Outputer)

    return inputer, processor, outputer

def load_module_after_init(directory):
    """有些任务是依赖_global里的数据，这里通常是在服务启动之后设置的"""
    if os.path.exists(os.path.join(directory, 'crontask.py')):
        import_by_abspath('crontask', os.path.join(directory, 'crontask.py'))


def go(task_dir):
    con_file = os.path.join(task_dir, "config.yaml")
    conf = get_conf(con_file)
    if 'gevent' in conf and conf.get('gevent'):
        from gevent import monkey
        monkey.patch_all()
        _global.GEVENT = True
    task_name = os.path.basename(task_dir)
    set_logger(conf)
    p, s, c = extract_worker_dir(task_dir)
    logging.info("fluent start!")
    from .scheduler import Scheduler
    m = Scheduler(conf, p, s, c, task_name=task_name)
    _global.SCHEDULER = m
    load_module_after_init(task_dir)
    m.start()
    logging.info("fluent exit!")


@click.group()
def main():
    pass


@click.group()
def stop():
    pass


@main.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('task')
@click.option('--extra', '-e',
              default=False,
              help="""
                    the argument you wish pass to fluent, for example:
                    --extra k1=v1,k2=v2
                    for using it:
                    ```
                    from fluent._global import EXTRA 
                    v1 = EXTRA.k1
                    ```
                    如果设置了env, 则会将_global.ENV改写为env, 目的是上报的数据做区分
                    """
              )
@click.option('--worker_name', '-w', default='', help="""worker name, use in report tag""")
def start(task, extra, worker_name):
    """启动程序

    Args:
        task:

    Returns:

    """
    _global.EXTRA = Extra(extra)
    if getattr(_global.EXTRA, 'env', ''):
        _global.ENV = _global.EXTRA.env
    if worker_name:
        _global.WORKER_NAME = worker_name
    go(task)


templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


@main.command(context_settings=dict(ignore_unknown_options=True))
def quickstart():
    """创建模板

    Returns:

    """
    project_name = click.prompt('请输入新建项目名')
    project_dir = os.path.abspath(click.prompt('请输入项目所在路径(将自动在该路径下创建一个文件夹({})'.format(project_name)))
    project_path = os.path.join(project_dir, project_name)
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    for filename in os.listdir(templates_path):
        filepath = os.path.join(templates_path, filename)
        if os.path.isfile(filepath):
            des_path = os.path.join(project_path, filename)
            shutil.copy(filepath, des_path)


if __name__ == '__main__':
    start()
