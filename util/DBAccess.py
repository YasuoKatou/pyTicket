# -*- coding:utf-8 -*-
import psycopg2
from psycopg2.extras import DictCursor
from config.db_config import DBConfig
from logging import getLogger

_Log = getLogger(__name__)

def Transactional(func):
    def wrapper(self, *args, **kwargs):
        _Log.debug('start Transactional')
        #DBに接続
        _Log.debug('DB URL : ' + DBConfig.getConnectUrl())
        with psycopg2.connect(dsn=DBConfig.getConnectUrl()) as conn:
            #トランザクション制御
            conn.autocommit = False
            try:
                #カーソルを開く
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    kwargs['cursor'] = cur
                    r = func(self, *args, **kwargs)
                conn.commit()
            except Exception as ex:
                _Log.error(str(ex))
                conn.rollback()
                r = {'status': 'NG', 'reason': str(ex)}
        kwargs['cursor'] = None
        _Log.debug('end Transactional')
        return r
    return wrapper
