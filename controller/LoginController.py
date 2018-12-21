# -*- coding:utf-8 -*-

import json
from bottle import HTTPResponse

from controller.BaseController import BaseController

class LoginController(BaseController):
    '''
    ログインコントローラクラス
    '''
    def __init__(self):
        '''
        URLのマッピング文字列を設定
        '''
        super().__init__('/login')
        pass
    def execute_post(self, request):
        '''
        ログイン処理を実行する.
        '''
        #ログインサービスを取得
        svc = super().get_service('login')
        #ログインサービスを実行
        r = svc.doLogin(request.json);
        #クライアントにログイン結果を戻す
        return super().edit_response(json.dumps(r))
#[EOF]