# -*- coding:utf-8 -*-

import json
from bottle import HTTPResponse
from logging import getLogger

from controller.BaseController import BaseController

_Log = getLogger(__name__)

class TicketHistoryController(BaseController):
    '''
    チケットコントローラクラス
    '''
    def __init__(self):
        '''
        URLのマッピングを設定
        '''
        mapping = [
            # チケット履歴一覧の取得
            {'url': '/ticket_history', 'method': 'ticketHistory'}]
        super().__init__('ticketHistory', mapping)

    def ticketHistory(self, request):
        '''
        チケット履歴一覧の取得
        '''
        # チケット履歴サービスを取得
        svc = super().get_service('ticketHistory')
        # 一覧取得サービスを呼び出し、
        svc_data = svc.findTicketHistory(request)
        '''
        svc_data = [
               {'id':1, 'root_id':1, 'parent_id':1, 'memo': 'memo #1'}
              ,{'id':2, 'root_id':2, 'parent_id':2, 'memo': 'memo #2'}
              ,{'id':3, 'root_id':3, 'parent_id':3, 'memo': 'memo #3'}
              ,{'id':4, 'root_id':2, 'parent_id':2, 'memo': 'memo #4'}
              ,{'id':5, 'root_id':1, 'parent_id':1, 'memo': 'memo #5'}
              ,{'id':6, 'root_id':2, 'parent_id':2, 'memo': 'memo #6'}
              ,{'id':7, 'root_id':2, 'parent_id':6, 'memo': 'memo #7'}
              ,{'id':8, 'root_id':2, 'parent_id':7, 'memo': 'memo #8'}
            ]
        '''
        # 一覧をクライアントに返信する
        return super().editOKResponse(svc_data)

#[EOF]