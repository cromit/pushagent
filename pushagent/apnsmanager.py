import gevent.ssl as ssl
from gevent.queue import Queue

import message

class APNSPool(object):
    def __init__(self, addr, key_file, cert_file, connections_num=3):
        self._connection_queue = Queue()
        self._addr = addr
        self._key_file = key_file
        self._cert_file = cert_file

    def start(self):
        conn = APNSConnector(self._addr, self._key_file, self._cert_file)
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
        '''
		self._feedback_connection = None
		self._sandbox = sandbox
		self._send_queue = Queue()
		self._error_queue = Queue()
		self._feedback_queue = Queue()
		self._send_greenlet = None
		self._error_greenlet = None
		self._feedback_greenlet = None

		self._send_queue_cleared = Event()
        '''

    def check_connection(self):
        if self._connection == None:
            print "Connect to APNS server addr[%s]" % (self._addr)
            sock = ssl.wrap_socket(socket(AF_INET, SOCK_STREAM, 0),
                self._key_file,
                self._cert_file,
                ssl_version=ssl.PROTOCOL_SSLv3)
            sock.connect_ex(tuple(self._addr.split(':')))
            self._connection = sock

    def send(self, message):
        # Send a push notification
        '''
        if not isinstance(message, PushMessage):
        raise ValueError, u"Message object should be a child of PushMessage."
        '''

        try:
            self._connection.send(str(msg))
        except Exception as err:
            self._connection.close()
            self._connection = None
            raise err
        




