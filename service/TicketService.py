# -*- coding:utf-8 -*-

import json
from logging import getLogger
from service.BaseService import BaseService

import util.DBAccess as DBA

_Log = getLogger(__name__)

class TicketService(BaseService):
    def __init__(self):
        super().__init__('ticket')

    @DBA.Transactional
    def findProjectTicket(self, request, *args, **kwargs):
        '''
        プロジェクトのチケット一覧取得を行う
        '''
        _Log.debug('findProjectTicket service start')
        cursor = kwargs['cursor']
        # チケットの検索
        dao = super().dao_manager.get_dao('ticketDao')
        p = {'pid': int(request.json['body']['project_id'])}
        r = dao.findByProject(cursor, p)
        # レスポンスの編集
        if r:
            if isinstance(r, list):
                return r
            else:
                return [r]
        else:
            return r

    @DBA.Transactional
    def findTicketMaster(self, request, *args, **kwargs):
        '''
        チケットマスタの取得を行う
        '''
        _Log.debug('findTicketMaster service start')
        cursor = kwargs['cursor']
        # チケットの検索
        dao = super().dao_manager.get_dao('ticketDao')
        p = {'pid': int(request.json['body']['project_id'])}
        recs = dao.findTicketMaster(cursor, p)
        # レスポンスの編集
        if not recs:
            return recs
        if not isinstance(recs, list):
            recs = [recs]
        r = {'status': [], 'progress': [], 'kind': [], 'priority': []}
        for rec in recs:
            r[rec['m_key']].append(rec)
        return {'master': r}

    @DBA.Transactional
    def newTicket(self, request, *args, **kwargs):
        '''
        チケットの登録
        '''
        _Log.debug('new ticket service start')
        cursor = kwargs['cursor']
        # ログイン情報を取得
        login = super().getLogin(cursor, request)

        # 最大のチケットIDを取得
        dao = super().dao_manager.get_dao('ticketDao')
        r = dao.findMaxId(cursor, {})
        maxId = r['max_id'] if r['max_id'] is not None else 0
        _Log.debug('max ticket id : ' + str(maxId))
        # チケットの登録
        tid = maxId + 1
        tinfo = request.json['body']
        #_Log.debug('new ticket request : ' + str(tinfo))
        tinfo['id'] = tid
        tinfo['createUserId'] = login['id']
        dao.addTicket(cursor, tinfo)

        # 最大のチケットメモIDを取得
        dao = super().dao_manager.get_dao('ticketMemoDao')
        r = dao.findMaxId(cursor, {})
        maxId = r['max_id'] if r['max_id'] is not None else 0
        _Log.debug('max ticket memo id : ' + str(maxId))
        # todo メモの登録
        mid = maxId + 1
        minfo = {'id': mid, 'ticket_id': tid, 'memo': '新規登録',
            'root_memo_id': mid, 'parent_memo_id': mid,
            'createUserId': login['id']}
        dao.addMemo(cursor, minfo)
        # レスポンスの編集
        return {'status': 'OK'}

#[EOF]