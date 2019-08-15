from mysql.connector import pooling

class DataConn(object):
    def __init__(self, db):
        self.cursor = db.cursor()
        self.database = db

    def close(self):
        self.cursor.close()
        self.database.close()


class PoolConn(object):
    def __init__(self, filestream, x):
        #self.filestream = filestream

        #with open(filestream, 'a+') as debug:
         #   debug.write('\nConnecting to database...')

        self._pool = pooling.MySQLConnectionPool(
            host="localhost",
            user="JacobDetwiler",
            passwd="L0adingg...",
            auth_plugin="mysql_native_password",
            database="db1",
            pool_size=x
        )

        self.connections = []
        self.__cons__ = x

    def get_connection(self):
        self.__cons__ -= 1
        if self.__cons__ < 0:
            return -1

        self.connections.append(DataConn(self._pool.get_connection()))

    def close_connection(self, db):
        if db != -1:
            self.__cons__ += 1
            db.close()