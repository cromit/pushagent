from __future__ import absolute_import
import os
import random
from pushagent.service import celery
from pushagent.message import *
import gevent

@celery.task
def send(target_id, message):
    from pushagent.service import apns_pool
    session = apns_pool.get_session()
    try:
        session.push(target_id, message)
    except Exception as err:
        print "Task::Send - err [%s]" % err
        raise

    apns_pool.return_session(session)
    '''
    apns_session = pushagent.apnmanager.get_session()
    apns_session.push(device_id, message)
    pushagent.apnsmanager.return_session(apns_session)
    sleep_time = random.random() * 5
    print "[%s] Send sleep %s" % (os.getpid(), sleep_time)
    gevent.sleep(sleep_time)
    print "[%s] Send wokeup" % os.getpid()
    '''

    return 

@celery.task
def add(x, y):
    global abc_instance
    print "PID %s abc %s abc.val %s" % (os.getpid(), abc_instance, abc_instance._val)
    abc_instance._val = random.random() * 10 
    print "==> PID %s abc %s abc.val %s" % (os.getpid(), abc_instance, abc_instance._val)
    return x + y

@celery.task
def mul(x, y):
    return x * y

@celery.task
def xsum(numbers):
    return sum(numbers)


@celery.task()
def A(how_many):
    from celery import group
    res = group(add.s(i, i) for i in xrange(how_many))()

    return 1

@celery.task()
def B(i):
    return pow2.delay(i)

@celery.task()
def pow2(i):
    return i ** 2

