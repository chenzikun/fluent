Fluent
===


# 概述

ETL是英文Extract-Transform-Load的缩写，用来描述将数据从来源端经过抽取（extract）、转换（transform）、加载（load）至目的端的过程

Fluent参照这个流程定义了inputer, process, output, scheduler 四个核心模块

* inputer 用于定义输入
* processor 用于定义中间处理
* outputer 用于用于定义输出
* scheduler 使用队列给上述三者传递数据，多线程启动，保证安全退出机制


# 安装

```sh 
    $ git clone http://git.code.oa.com/yoyoyo/fluent.git
    $ pip3 install .
```

# 使用方式  


**1. 创建文件**

```sh
$ fluent quickstart
$ 请输入新建项目名:
$ test
$ 请输入项目所在路径(将自动在该路径下创建一个文件夹(test)
$ ./
```

**2. 编写项目**

**3. 运行程序**

```sh
fluent start project_name   
```

# 终断信号

不能使用 `kill -9 PID` 去终止进程，因为数据在队列中缓冲，需要等待现有数据消费完，除非打算丢弃队列中的数据.

应使用以下方式:

* ctrl + c
* `kill -2 PID`
* 使用 `supervisorctl start or stop project`

# Links

* Documents: [http://dev.cms.joox.ibg.com/docs/fluent/index.html](https://test.cms.joox.ibg.com/docs/fluent/index.html)
* Code: [https://git.code.oa.com/yoyoyo/fluent](https://git.code.oa.com/yoyoyo/fluent)

# todo 

* 跟踪数据流（log, id）
* 支持测试