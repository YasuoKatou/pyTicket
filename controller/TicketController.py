# -*- coding:utf-8 -*-

import json
from bottle import HTTPResponse

from controller.BaseController import BaseController

class TicketController(BaseController):
    '''
    チケットコントローラクラス
    '''
    def __init__(self):
        '''
        URLのマッピングを設定
        '''
        mapping = [
            # プロジェクトのチケット一覧の取得
            {'url': '/ticket_list', 'method': 'ticketList'},
            # チケットのマスタを取得
            {'url': '/ticket_master', 'method': 'ticketMaster'},
            # チケットの登録
            {'url': '/new_ticket', 'method': 'newTicket'},
            # チケットの更新
            {'url': '/edit_ticket', 'method': 'editTicket'},
            # チケット詳細取得
            {'url': '/ticket_detail', 'method': 'ticketDetail'}]
        super().__init__('ticket', mapping)

    def ticketList(self, request):
        '''
        プロジェクトのチケット一覧の取得
        '''
        # チケットサービスを取得
        svc = super().get_service('ticket')
        # 一覧取得サービスを呼び出し、
        svc_data = svc.findProjectTicket(request)
        # 一覧をクライアントに返信する
        return super().editOKResponse(svc_data)

    def ticketMaster(self, request):
        '''
        チケットのマスタを取得
        '''
        # チケットサービスを取得
        svc = super().get_service('ticket')
        # チケットマスタ取得サービスを呼び出し、
        svc_data = svc.findTicketMaster(request)
        # 結果をクライアントに返信する
        return super().editOKResponse(svc_data)


    def newTicket(self, request):
        '''
        チケットの登録
        '''
        # todo 実装
        pass

    def editTicket(self, request):
        '''
        チケットの更新
        '''
        # todo 実装
        pass

    def ticketDetail(self, request):
        '''
        チケット詳細取得
        '''
        # todo 実装
        pass
#[EOF]