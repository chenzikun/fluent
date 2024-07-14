import gevent
import gevent.pool

pool = gevent.pool.Pool(5)
def test2():
    gevent.sleep(1)
    print('test2', gevent.getcurrent())

def test():
    gevent.sleep(1)
    pool = gevent.pool.Pool(5)
    gs = [pool.spawn(test2) for i in range(10)]
    gevent.joinall(gs)
    print('test1', gevent.getcurrent())
def start():
    gs = [pool.spawn(test) for i in range(10)]
    gevent.joinall(gs)


start()
