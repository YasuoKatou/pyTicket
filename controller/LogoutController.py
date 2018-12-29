# -*- coding:utf-8 -*-

from controller.BaseController import BaseController

class LogoutController(BaseController):
    '''
    ログアウトコントローラクラス
    '''
    def __init__(self):
        '''
        URLのマッピングを設定
        '''
        mapping = [
            # ログアウト処理
            {'url': '/logout', 'method': 'doLogout'}]
        super().__init__('logout', mapping)

    def doLogout(self, request):
        '''
        ログアウト処理を実行する.
        '''
        #TODO ログアウト処理を実装すること
        print('start logout controller')
#[EOF]