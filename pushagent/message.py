import tasks

class PushMessage(object):
    TYPE_UNDEFINED=0
    TYPE_GCM=1
    TYPE_APN=2

    @classmethod
    def get_result(cls, result_id):
        from pushagent.service import celery
        res = celery.AsyncResult(result_id)
        return res.state

    def __init__(self, provider_type=TYPE_UNDEFINED, device_id=None, alert=None, badge=None, sound=None, identifier=0, expiry=None, extra=None):
        self._type=provider_type
        pass

    def send(self):
        # Send the messages according to priority
        result = tasks.send.delay(10, 10)
        print result.collect()

        return result.id

class APushMessage(PushMessage):
    def __init__(self, device_id, alert=None, badge=None, sound=None, identifier=0, expiry=None, extra=None):
        self._type=TYPE_APN
        pass

    def send(self):
        pass

class GPushMessage(PushMessage):
    def __init__(self, device_id, alert=None, badge=None, sound=None, identifier=0, expiry=None, extra=None):
        self._type=TYPE_GCM
        pass

    def send(self):
        pass
