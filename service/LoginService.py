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
        #ログイン用セッションIDを取得
        sessionDao = super().dao_manager.get_dao('sessionDao')
        ts = sessionDao.execute(kwargs['cursor'], 'findByPk', {'session_id': sid})
        if ts is None:
            #ログイン用セッションIDが取得できなかった場合
            raise Exception('no temp session id')
        _Log.debug('temp session id : ' + ts['session_id'])
        if ts['session_id'] != sid:
            #異なるログイン用セッションIDを取得
            raise Exception('temp session id wrong !?')
        #todo ユーザIDとパスワードを復号
        dec_login_id = decryption(sid[:16], login_id)
        #_Log.debug('source  : ' + dec_login_id.hex())
        #todo ユーザIDとパスワードを確認
        #todo 正式なセッションIDを作成し、登録
        '''
        sid = rand_n()
        rec = {'session_id':sid, 'user_id':login_id, 'createUserId':1}
        dao.execute(kwargs['cursor'], 'insert', rec)
        '''
        #todo ログイン用セッションIDを削除
        '''
        sessionDao.execute(kwargs['cursor'], 'deleteByPk', {'session_id': sid})
        '''
        return {'message': 'hello ' + login_id}
#[EOF]
