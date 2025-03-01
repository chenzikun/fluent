.. _quickstart:

quickstart
===========


1. Create job with templates
-----------------------------

使用模板创建任务

.. code-block:: shell

    $ fluent quickstart
    $ 请输入新建项目名:
    $ test
    $ 请输入项目所在路径(将自动在该路径下创建一个文件夹(test)
    $ ./

此时当前目录下创建了文件夹test

.. code-block:: shell

    $ ls test
    config.yaml input.py    output.py   process.py   __init__.py


2. Start job
-------------

定义程序

.. code-block:: python
    :caption: ``inputer.py``

    from fluent.core import Inputer

    class UserInputer(Inputer):
        """用户定义handle_item"""

        def handle_item(self):
            """"""
            return 1


启动程序

.. code-block:: sh

    $ fluent start test


3. 启动参数
--------------
.. code-block:: sh

    $ fluent start test --extra env=test,name=test

.. code-block:: python

    # 使用启动参数
    from fluent import _global
    env = _global._EXTRA.env
    name = _global._EXTRA.name


4. Attention
--------------


.. note::

    不能使用 ``kill -9 PID`` 去终止进程，因为数据在队列中缓冲，需要等待现有数据消费完，除非打算丢弃内存队列中的数据

    应使用以下方式:

    * Ctrl + C
    * ``kill -2 PID``
    * 使用 ``supervisorctl start or stop project``
    * 使用弹性线程时，线程会动态创建退出, 需要注意是否有内存泄漏


