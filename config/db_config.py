# -*- coding:utf-8 -*-

DBType_SQLite = 'SQLite'
DBType_PostgreSQL = 'PostgreSQL'
_DBType = DBType_SQLite

_DB_URL_SQLite = u'C:\\Users\\YasuoKatou\\Documents\\workspaces\\sqlite3\\sticket.db'
_DB_URL_PostgreSQL = 'postgresql://ticket-admin:TicketAdmin@192.168.3.172:5432/ticket'
_DB_URL = _DB_URL_SQLite

class DBConfig:
    @staticmethod
    def getDBType():
        return _DBType
    @staticmethod
    def getConnectUrl():
        return _DB_URL
#[EOF]