# -*- coding:utf-8 -*-

import json
from service.BaseService import BaseService
from util.DBAccess import Transactional

from util.MyRandom import rand_n

class LoginService(BaseService):
    def __init__(self):
        super().__init__('login')

    @Transactional
    def prepareLogin(self, *args, **kwargs):
        print('login prepared service start')
        #print('args', args)
        #print('kwargs', kwargs)
        sid = rand_n()
        dao = super().dao_manager.get_dao('sessionDao')
        rec = {'session_id':sid, 'user_id':None, 'createUserId':1}
        dao.execute(kwargs['cursor'], 'insert', rec)
        print ('insert', sid)
        return {'session_id': sid}

    @Transactional
    def doLogin(self, request, *args, **kwargs):
        print('type of request :', type(request))
        key_user_id = 'user_id'
        user_id = request[key_user_id]
        print(key_user_id, ":", user_id)
        return {'message': 'hello ' + user_id}
#[EOF]