# -*- coding:utf-8 -*-
import sqlite3

from config.db_config import DBConfig
from logging import getLogger

_Log = getLogger(__name__)

def Transactional(func):
    def wrapper(*args, **kwargs):
        #_Log.debug('start Transactional')
        #DBに接続
        #_Log.debug('DB URL : ' + DBConfig.getConnectUrl())
        with sqlite3.connect(DBConfig.getConnectUrl(), isolation_level='EXCLUSIVE') as conn:
            #トランザクション制御
            #conn.autocommit = False    #これは、PostgreSQL(psycopg2)の設定
            try:
                #カーソルを開く
                '''
                with conn.cursor() as cur:
                    kwargs['cursor'] = cur
                    #r = func(self, *args, **kwargs)
                    r = func(*args, **kwargs)
                '''
                cur = conn.cursor()     # SQLiteでは、withが使えない
                kwargs['cursor'] = cur
                r = func(*args, **kwargs)

                conn.commit()
            except Exception as ex:
                _Log.error(str(ex))
                conn.rollback()
                r = {'status': 'NG', 'reason': str(ex)}
        kwargs['cursor'] = None
        _Log.debug('end Transactional')
        return r
    return wrapper

#[EOF]