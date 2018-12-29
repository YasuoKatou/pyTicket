# -*- coding:utf-8 -*-
import psycopg2
from config.db_config import DBConfig

def Transactional(func):
    def wrapper(self, *args, **kwargs):
        print('start Transactional')
        #DBに接続
        print('DB URL :', DBConfig.getConnectUrl())
        with psycopg2.connect(DBConfig.getConnectUrl()) as conn:
            #トランザクション制御
            conn.autocommit = False
            try:
                #カーソルを開く
                with conn.cursor() as cur:
                    kwargs['cursor'] = cur
                    r = func(self, *args, **kwargs)
                conn.commit()
            except Exception as ex:
                print(ex)
                conn.rollback()
        kwargs['cursor'] = None
        print('end Transactional')
        return r
    return wrapper