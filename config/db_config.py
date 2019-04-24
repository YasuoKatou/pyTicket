# -*- coding:utf-8 -*-

DBType_SQLite = 'SQLite'
DBType_PostgreSQL = 'PostgreSQL'
#_DBType = DBType_SQLite
_DBType = DBType_PostgreSQL

_DB_SERVER = '192.168.3.197'
_DB_SERVER_PORT = '5432'
_DB_URL_SQLite = u'C:\\Users\\YasuoKatou\\Documents\\workspaces\\sqlite3\\ticket.db'
_DB_URL_PostgreSQL = u'postgresql://ticket-admin:TicketAdmin@{}:{}/ticket'
#_DB_URL = _DB_URL_SQLite
_DB_URL = _DB_URL_PostgreSQL

class DBConfig:
    @staticmethod
    def getDBType():
        return _DBType
    @staticmethod
    def setDBServer(svr):
        global _DB_SERVER
        _DB_SERVER = svr
    @staticmethod
    def setDBServerPort(port):
        global _DB_SERVER_PORT
        _DB_SERVER_PORT = port
    @staticmethod
    def getConnectUrl():
        if _DBType == DBType_PostgreSQL:
            print(_DB_URL_PostgreSQL.format(_DB_SERVER, _DB_SERVER_PORT))
            return _DB_URL_PostgreSQL.format(_DB_SERVER, _DB_SERVER_PORT)
        else:
            return _DB_URL
#[EOF]