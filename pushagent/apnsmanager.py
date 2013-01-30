import struct
import gevent.ssl as ssl
from gevent.queue import Queue
from gevent.socket import *

import message

class APNSPushSessionPool(object):
    def __init__(self, addr, key_file, cert_file):
        self._connection_queue = Queue()
        self._addr = addr
        self._key_file = key_file
        self._cert_file = cert_file

    def start(self, concurrency=3):
        for x in range(0, concurrency):
            conn = APNSPushSession(self._addr, self._key_file, self._cert_file)
            self._connection_queue.put(conn)
            conn.check_connection()

    def get_session(self):
        conn = self._connection_queue.get()
        conn.check_connection()

        return conn

    def return_session(self, conn):
        self._connection_queue.put(conn)

class APNSConnector(object):
    def __init__(self, addr, key_file, cert_file):
        self._connection = None
        self._addr = addr
        self._key_file = key_file 
        self._cert_file = cert_file

    def check_connection(self):
        if self._connection == None:
            print "Connect to APNS server addr[%s]" % (self._addr)
            sock = ssl.wrap_socket(socket(AF_INET, SOCK_STREAM, 0),
                self._key_file,
                self._cert_file,
                ssl_version=ssl.PROTOCOL_SSLv3)
            host, port  = self._addr.split(':')
            sock.connect_ex((host, int(port)))
            self._connection = sock

    def close(self):
        print "Close connection"
        self._connection.close()
        self._connection = None

class APNSPushSession(APNSConnector):
    def push(self, target_id, message):
        # Send a push notification
        from pushagent.message import APushMessage
        if not isinstance(message, APushMessage):
            raise ValueError, u"Message object should be a child of PushMessage."

        message._token = target_id.decode("hex")
        #print "Actual Sending %s" % str(message)
        try:
            self._connection.send(str(message))
        except Exception as err:
            self._connection.close()
            self._connection = None
            print "Send exception %s" % err
            raise err
        print "Sent message"

class APNSFeedbackSubscriber(APNSConnector):
    def start(self):
        self.check_connection()

        import gevent
        gevent.spawn(self.receive_feedback)
        
    def receive_feedback(self):
        print "Receiving..."
        while True:
            try:
                msg = self._connection.recv(4 + 2 + 32)
                if len(msg) < 38:
                    return
                data = struct.unpack("!IH32s", msg)
                print "Received data [%s]" % data
            except Exception as err:
                self._connection.close()
                self._connection = None
                print "Recv exception %s" % err
                raise err

        print "Receive end"


