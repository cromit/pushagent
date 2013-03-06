import struct
import gevent
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
            print "Connecting to server[%s]" % (self._addr)
            sock = ssl.wrap_socket(socket(AF_INET, SOCK_STREAM, 0),
                self._key_file,
                self._cert_file,
                ssl_version=ssl.PROTOCOL_SSLv3)
            host, port  = self._addr.split(':')
            ret = sock.connect_ex((host, int(port)))
            if ret == 0:
                print "Connection established to addr[%s]" % (self._addr)
                self._connection = sock
                return True
            print "Connecting failed to addr[%s]" % (self._addr)

            return False
        return True

    def close(self):
        print "Close connection"
        if self._connection:
            self._connection.close()
            self._connection = None

class APNSPushSession(APNSConnector):
    def push(self, target_id, message):
        # Send a push notification
        if self.check_connection() == False:
            raise IOError, u'Connection is not established'

        from pushagent.message import APushMessage
        if not isinstance(message, APushMessage):
            raise ValueError, u"Message object should be a child of PushMessage."

        message._token = target_id.decode("hex")
        #print "Actual Sending %s" % str(message)
        try:
            self._connection.send(str(message))
        except Exception as err:
            self.close()
            print "Send exception %s" % err
            raise err
        print "Sent message"

class APNSFeedbackSubscriber(APNSConnector):
    def __init__(self, addr, key_file, cert_file, check_period, feedback_storage):
        super(APNSFeedbackSubscriber, self).__init__(addr, key_file, cert_file)
        self._storage = feedback_storage
        self._check_period = check_period

    def start(self):
        gevent.spawn(self.receive_feedback)

    def check_connection(self):
        if self._connection == None:
            print "Connecting to server[%s]" % (self._addr)
            sock = socket(AF_INET, SOCK_STREAM, 0)
            host, port  = self._addr.split(':')
            ret = sock.connect_ex((host, int(port)))
            if ret == 0:
                print "Connection established to addr[%s]" % (self._addr)
                self._connection = sock
                return True

            print "Connecting failed to addr[%s]" % (self._addr)
            return False

        return True
        
    def receive_feedback(self):
        while True:
            try:
                if self.check_connection():
                    print "Receiving feedback..."
                    msg = self._connection.recv(4 + 2 + 32)
                    if len(msg) < 38:
                        print "Wrong data size [%s]" % len(msg)
                        self.close()
                        gevent.sleep(self._check_period)
                        continue

                    data = struct.unpack("!IH32s", msg)
                    print "Received data [%s]" % data[2]
                    self._storage.store(data[2])
                else:
                    print "Try connecting again after a while.."
                    gevent.sleep(self._check_period) 

            except Exception as err:
                print "Recv exception %s" % err
                self.close()
                raise

        print "Receive end"

