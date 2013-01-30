import time, json, struct

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

class APushMessage(PushMessage):
    def __init__(self, alert=None, badge=1, sound='default', identifier=0, expiry=None, extra=None):
        """
        Inititalizes a message for APNS

        device_id - device token
        alert - message string or message dictionary
        badge - badge number
        sound - name of sound to play
        identifier - message identifier
        expiry - expiry date of message
        extra - dictionary of extra parameters
        """
        #if len(device_id) != 32:
            #raise ValueError, u"Token must be a 32-byte binary string."
        if (alert is not None) and (not isinstance(alert, (str, unicode, dict))):
            raise ValueError, u"Alert message must be a string or a dictionary."
        if expiry is None:
            expiry = long(time.time() + 365 * 86400)

        self._token = ''
        self._type = self.TYPE_APN
        self._alert = alert
        self._badge = badge
        self._sound = sound
        self._identifier = identifier
        self._expiry = expiry
        self._extra = extra

    def __str__(self):
        aps = { "alert" : self._alert }
        if self._badge is not None:
            aps["badge"] = self._badge
        if self._sound is not None:
            aps["sound"] = self._sound

        data = { "aps" : aps }
        if self._extra is not None:
            data.update(self._extra)

        encoded = json.dumps(data)
        length = len(encoded)

        return struct.pack("!bIIH32sH%(length)ds" % { "length" : length },
            1, self._identifier, self._expiry,
            32, self._token, length, encoded)


class GPushMessage(PushMessage):
    def __init__(self, device_id, alert=None, badge=None, sound=None, identifier=0, expiry=None, extra=None):
        self._type=TYPE_GCM
        pass

    def send(self):
        pass
