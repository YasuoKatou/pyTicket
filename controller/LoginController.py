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
            {'url': '/login', 'method': 'doLogin'},
            # ログアウト処理
            {'url': '/logout', 'method': 'doLogout'}]
        super().__init__('login', mapping)

    def doPreapre(self, request):
        '''
        ログイン前処理を実行する.
        $ curl -X POST http://localhost:8080/login/prepare
        '''
        #ログインサービスを取得
        svc = super().get_service('login')
        #ログイン前処理を実行
        r = svc.prepareLogin()
        #クライアントに結果を戻す
        return r

    def doLogin(self, request):
        '''
        ログイン処理を実行する.
        curl -H "Content-Type: application/json" -X POST -d '{ "login_id" : "xxx", "passwd": "yyy", "session_id": "f95f13565E18520D702f5d1F3C7A4aB02a437282e784fFD0D58cdBb89Ea21BF5" }' http://localhost:8080/login
        '''
        #ログインサービスを取得
        svc = super().get_service('login')
        #ログイン処理を実行
        r = svc.doLogin(request.json);
        #クライアントにログイン結果を戻す
        return r

    def doLogout(self, request):
        '''
        ログアウト処理を実行する.
        '''
        #ログインサービスを取得
        svc = super().get_service('login')
        #ログアウト処理を実行
        r = svc.doLogout(request.json);
        #クライアントにログアウト結果を戻す
        return r
#[EOF]
