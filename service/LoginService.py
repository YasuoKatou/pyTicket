# -*- coding:utf-8 -*-

import json
from logging import getLogger
from service.BaseService import BaseService
from util.DBAccess import Transactional

from util.MyRandom import rand_n
from util.MyEncryption import decryption

_Log = getLogger(__name__)

class LoginService(BaseService):
    def __init__(self):
        super().__init__('login')

    @Transactional
    def prepareLogin(self, *args, **kwargs):
        _Log.debug('login prepared service start')
        sid = rand_n()
        dao = super().dao_manager.get_dao('sessionDao')
        rec = {'session_id':sid, 'user_id':None, 'createUserId':1}
        dao.execute(kwargs['cursor'], 'insert', rec)
        _Log.debug('insert : ' + sid)
        return {'session_id': sid}

    @Transactional
    def doLogin(self, request, *args, **kwargs):
        _Log.debug('login service start')
        sid = request['session_id']
        login_id = request['login_id']
        passwd   = request['passwd']
        cursor = kwargs['cursor']
        #-------------------------------
        #ログイン用セッションIDを取得
        sessionDao = super().dao_manager.get_dao('sessionDao')
        ts = sessionDao.execute(cursor, 'findByPk', {'session_id': sid})
        if ts is None:
            #ログイン用セッションIDが取得できなかった場合
            raise Exception('no temp session id')
        _Log.debug('temp session id : ' + ts['session_id'])
        if ts['session_id'] != sid:
            #異なるログイン用セッションIDを取得
            raise Exception('temp session id wrong !?')
        #-------------------------------
        #ユーザIDとパスワードを復号
        try:
            dec_key = sid[:16]
            dec_login_id = decryption(dec_key, login_id)
            #_Log.debug('login_id source : ' + dec_login_id)
            dec_passwd = decryption(dec_key, passwd)
            #_Log.debug('passwd source : ' + dec_passwd)
        except Exception as ex:
            _Log.error(str(ex))
            raise Exception('decryption error')
        #-------------------------------
        #ユーザIDとパスワードを確認
        userMasterDao = super().dao_manager.get_dao('userMasterDao')
        um = userMasterDao.execute(cursor, 'findByLoginId', {'login_id': dec_login_id})
        if um is None:
            #ユーザマスタが取得できなかった場合
            raise Exception('no user master')
        if um['passwd'] != dec_passwd:
            #パスワードが不一致の場合
            raise Exception('password error')
        #-------------------------------
        #正式なセッションIDを作成し、登録
        new_sid = rand_n()
        rec = {'session_id':new_sid, 'user_id':dec_login_id, 'createUserId':1}
        sessionDao.execute(cursor, 'insert', rec)
        _Log.debug('new session id : ' + new_sid)
        #-------------------------------
        #ログイン用セッションIDを削除
        sessionDao.execute(cursor, 'deleteByPk', {'session_id': sid})

        return {'session_id': new_sid}

    @Transactional
    def doLogout(self, request, *args, **kwargs):
        sessionDao = super().dao_manager.get_dao('sessionDao')
        cursor = kwargs['cursor']
        sid = request['session_id']
        sessionDao.execute(cursor, 'deleteByPk', {'session_id': sid})
        _Log.debug('delete session id : ' + sid)
        return {'result': True}
#[EOF]
