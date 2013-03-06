
class UDeviceStorageFactory(object):
    @classmethod
    def create(cls, store_type, store_path):
        if store_type == 'sqlite':
            return SQLiteUDeviceStorage(store_path)

class UDeviceStorage(object):
    def store(self, device_id):
        raise NotImplementedError

class SQLiteUDeviceStorage(object):
    def __init__(self, store_path):
        self._store_path = store_path
        
        print "Initialize 'sqlite' feedback storage"
        import sqlite3 as sqlite
        self._conn = sqlite.connect(self._store_path, isolation_level=None)

        cur = self._conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='unregistered_devices_ios'")

        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute("""
                    CREATE TABLE unregistered_devices_ios (
                        time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        device_token BLOB 
                        );
                """)
            cur.execute("CREATE INDEX unregistered_devices_ios_idx ON unregistered_devices_ios(time);")
            self._conn.commit()
        cur.close()

    def store(self, device_id):
        import sqlite3 as sqlite
        cur = self._conn.cursor()
        print "STORE [%s] - [%s]" % (device_id, device_id.encode('hex'))
        cur.execute("INSERT INTO unregistered_devices_ios(time, device_token) VALUES( datetime(), ? )", [sqlite.Binary(device_id)])
        self._conn.commit()
        cur.close()

    def get_all(self):
        print "Getting all data"
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM unregistered_devices_ios")

        result = []
        print "Iterate cursor"
        while True:
            row = cur.fetchone() 
            if row == None:
                break 

            result.append((str(row[0]), str(row[1]).encode('hex')))

        print result

        cur.close()

    def clear(self):
        print "Clear Table"
        cur = self._conn.cursor()
        cur.execute("DELETE FROM unregistered_devices_ios")
        self._conn.commit()
        cur.close()

