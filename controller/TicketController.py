# -*- coding:utf-8 -*-

import json
from bottle import HTTPResponse
from logging import getLogger

from controller.BaseController import BaseController

_Log = getLogger(__name__)

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
        svc_data = svc.findTicketMaster(request.json['body']['project_id'])
        # 結果をクライアントに返信する
        return super().editOKResponse(svc_data)


    def newTicket(self, request):
        '''
        チケットの登録
        '''
        # チケットサービスを取得
        svc = super().get_service('ticket')
        # チケットを登録し、
        svc_result = svc.newTicket(request)
        # 登録結果をクライアントに返信する
        if svc_result['status'] == 'OK':
            return super().editOKResponse(None)
        else:
            return super().editNGResponse(svc_result['reason'])

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
        # チケットサービスを取得
        svc = super().get_service('ticket')
        svc_data = {}
        # 詳細取得サービスを呼び出し、
        svc_data['ticket'] = svc.ticketDetail(request)
        # チケットマスタ取得サービスを呼び出し、
        pid = str(svc_data['ticket']['project_id'])
        svc_data['master'] = svc.findTicketMaster(pid)['master']
        # 詳細情報をクライアントに返信する
        return super().editOKResponse(svc_data)
#[EOF]