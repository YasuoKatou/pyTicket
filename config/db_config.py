# -*- coding:utf-8 -*-

DBType_SQLite = 'SQLite'
DBType_PostgreSQL = 'PostgreSQL'
#_DBType = DBType_SQLite
_DBType = DBType_PostgreSQL

_DB_URL_SQLite = u'C:\\Users\\YasuoKatou\\Documents\\workspaces\\sqlite3\\ticket.db'
_DB_URL_Postgre_RasPI = u'postgresql://ticket-admin:TicketAdmin@192.168.3.6:5432/ticket'
_DB_URL_PostgreSQL = _DB_URL_Postgre_RasPI
#_DB_URL = _DB_URL_SQLite
_DB_URL = _DB_URL_PostgreSQL

class DBConfig:
    @staticmethod
    def getDBType():
        return _DBType
    @staticmethod
    def getConnectUrl():
        return _DB_URL
#[EOF]