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
        URLのマッピングを設定
        '''
        mapping = [
            # ログイン前処理
            {'url': '/login/prepare', 'method': 'doPreapre'},
            # ログイン処理
            {'url': '/login', 'method': 'doLogin'}]
        super().__init__('login', mapping)

    def doPreapre(self, request):
        '''
        ログイン前処理を実行する.
        $ curl -X POST http://localhost:8080/login/prepare
        '''
        #ログインサービスを取得
        svc = super().get_service('login')
        #ログイン前処理サービスを実行
        r = svc.prepareLogin()
        #クライアントに結果を戻す
        return super().edit_response(json.dumps(r))

    def doLogin(self, request):
        '''
        ログイン処理を実行する.
        curl -H "Content-Type: application/json" -X POST -d '{ "user_id" : "yasuo katou" }' http://localhost:8080/login
        '''
        #ログインサービスを取得
        svc = super().get_service('login')
        #ログインサービスを実行
        r = svc.doLogin(request.json);
        #クライアントにログイン結果を戻す
        return super().edit_response(json.dumps(r))
#[EOF]