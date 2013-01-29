from __future__ import absolute_import
from celery import Celery
from pushagent import agent_conf

celery = Celery(include=['pushagent.tasks'])
celery.config_from_object(agent_conf)

print "Celery configured"

'''
if __name__ == '__main__':
    celery.start()
'''
