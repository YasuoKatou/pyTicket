# -*- coding:utf-8 -*-

import json
from logging import getLogger
from service.BaseService import BaseService

from util.MyRandom import rand_n
from util.MyEncryption import decryption

import util.DBAccess as DBA

_Log = getLogger(__name__)

class LoginService(BaseService):
    def __init__(self):
        super().__init__('login')

    @DBA.Transactional
    def prepareLogin(self, *args, **kwargs):
        _Log.debug('login prepare service start')
        sid = rand_n()
        dao = super().dao_manager.get_dao('sessionDao')
        rec = {'session_id':sid, 'user_id':None, 'createUserId':1}
        dao.insert(kwargs['cursor'], rec)
        _Log.debug('insert : ' + sid)
        return {'session_id': sid}

    @DBA.Transactional
    def doLogin(self, request, *args, **kwargs):
        _Log.debug('login service start')
        sid = request['header']['session_id']
        request_body = request['body']
        login_id = request_body['login_id']
        passwd   = request_body['passwd']
        cursor = kwargs['cursor']
        #-------------------------------
        #ログイン用セッションIDを取得
        sessionDao = super().dao_manager.get_dao('sessionDao')
        ts = sessionDao.findByPk(cursor, {'session_id': sid})
        if ts is None:
            #ログイン用セッションIDが取得できなかった場合
            _Log.error('no temp session id : ' + sid)
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
        um = userMasterDao.findByLoginId(cursor, {'login_id': dec_login_id})
        if um is None:
            #ユーザマスタが取得できなかった場合
            _Log.error('no user master : ' + dec_login_id)
            raise Exception('no user master')
        if um['passwd'] != dec_passwd:
            #パスワードが不一致の場合
            raise Exception('password error')
        #-------------------------------
        #正式なセッションIDを作成し、登録
        new_sid = rand_n()
        rec = {'session_id':new_sid, 'user_id':um['id'], 'createUserId':1}
        sessionDao.insert(cursor, rec)
        _Log.debug('new session id : ' + new_sid)
        #-------------------------------
        #ログイン用セッションIDを削除
        sessionDao.deleteByPk(cursor, {'session_id': sid})

        return {'session_id': new_sid}

    @DBA.Transactional
    def doLogout(self, request, *args, **kwargs):
        sessionDao = super().dao_manager.get_dao('sessionDao')
        cursor = kwargs['cursor']
        sid = request['session_id']
        sessionDao.deleteByPk(cursor, {'session_id': sid})
        _Log.debug('delete session id : ' + sid)
        return {'result': True}
#[EOF]