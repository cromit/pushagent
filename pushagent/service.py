from __future__ import absolute_import
from celery import Celery
from pushagent import agent_conf
from celery.signals import worker_init 

celery = Celery(include=['pushagent.tasks'])
celery.config_from_object(agent_conf)
print "Celery configured"

apns_pool = None
apns_subscriber = None

@worker_init.connect
def on_worker_init(sender=None, conf=None, **kwds):
    global apns_pool, apns_subscriber
    print "worker init"

    from pushagent.apnsmanager import APNSPushSessionPool
    apns_pool = APNSPushSessionPool(agent_conf.APNS_PUSH_GATEWAY_URL, agent_conf.APNS_KEY_FILE, agent_conf.APNS_CERT_FILE)
    apns_pool.start()

    from pushagent.apnsmanager import APNSFeedbackSubscriber
    apns_subscriber = APNSFeedbackSubscriber(agent_conf.APNS_FEEDBACK_GATEWAY_URL, agent_conf.APNS_KEY_FILE, agent_conf.APNS_CERT_FILE)
    apns_subscriber.start()


'''
if __name__ == '__main__':
    celery.start()
'''
