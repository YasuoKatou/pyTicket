# -*- coding:utf-8 -*-

from controller.BaseController import BaseController

class LogoutController(BaseController):
    '''
    ログアウトコントローラクラス
    '''
    def __init__(self):
        '''
        URLのマッピング文字列を設定
        '''
        super().__init__('/logout')

    def execute_post(self, request):
        '''
        ログアウト処理を実行する.
        '''
        #TODO ログアウト処理を実装すること
        print('start logout controller')
#[EOF]