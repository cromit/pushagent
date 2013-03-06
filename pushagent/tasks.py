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
    finally:
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
