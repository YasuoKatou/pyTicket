# -*- coding:utf-8 -*-

import json
from service.BaseService import BaseService

class LoginService(BaseService):
    def __init__(self):
        super().__init__('login')
    def doLogin(self, request):
        print('type of request :', type(request))
        key_user_id = 'user_id'
        user_id = request[key_user_id]
        print(key_user_id, ":", user_id)
        return {'message': 'hello ' + user_id}
#[EOF]