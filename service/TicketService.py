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

#[EOF]