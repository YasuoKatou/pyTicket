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
    def findTicketMaster(self, project_id, *args, **kwargs):
        '''
        チケットマスタの取得を行う
        '''
        _Log.debug('findTicketMaster service start')
        cursor = kwargs['cursor']
        # チケットの検索
        dao = super().dao_manager.get_dao('ticketDao')
        p = {'pid': int(project_id)}
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
        # メモの登録
        mid = maxId + 1
        minfo = {'id': mid, 'ticket_id': tid, 'memo': '新規登録',
            'root_memo_id': mid, 'parent_memo_id': mid,
            'createUserId': login['id']}
        dao.addMemo(cursor, minfo)
        # レスポンスの編集
        return {'status': 'OK'}

    @DBA.Transactional
    def ticketDetail(self, request, *args, **kwargs):
        '''
        チケット詳細取得
        '''
        _Log.debug('ticket detail service start')
        cursor = kwargs['cursor']
        dao = super().dao_manager.get_dao('ticketDao')
        r = dao.findById(cursor, {'tid': int(request.json['body']['ticket_id'])})
        r['start_date'] = super().strfdate(r['start_date'])
        r['finish_date'] = super().strfdate(r['finish_date'])
        r['last_update'] = super().strftime(r['last_update'])
        return r

    def _makeDiff(self, ol, nw):
        '''
        更新履歴を編集する
        '''
        def _check(key):
            olw = ol[key] if ol[key] else '未設定'
            nww = nw[key] if nw[key] else '未設定'
            if olw != nww:
                return '【{0}】--> 【{1}】'.format(olw, nww)
            return None
        def _dateCheck(key):
            olw = str(ol[key]) if ol[key] else '未設定'
            nww = str(nw[key]) if nw[key] else '未設定'
            if olw != nww:
                return '【{0}】--> 【{1}】'.format(olw, nww)
            return None

        m = []
        #タイトル
        n = _check('title')
        if n:
            m.append('タイトルを変更 ' + n)
        #内容
        n = _check('description')
        if n:
            m.append('説明を変更 ' + n)
        #状態
        n = _check('status_name')
        if n:
            m.append('状態を変更 ' + n)
        #進捗
        n = _check('progress_name')
        if n:
            m.append('進捗を変更 ' + n)
        #種類
        n = _check('kind_name')
        if n:
            m.append('種類を変更 ' + n)
        #優先順位
        n = _check('priority_name')
        if n:
            m.append('優先順位を変更 ' + n)
        #開始日
        n = _dateCheck('start_date')
        if n:
            m.append('開始日を変更 ' + n)
        #終了日
        n = _dateCheck('finish_date')
        if n:
            m.append('終了日を変更 ' + n)

        if len(m) > 0:
            return '\n'.join(m)
        else:
            return '変更なし'

    @DBA.Transactional
    def updateTicket(self, request, *args, **kwargs):
        '''
        チケット更新
        '''
        _Log.debug('ticket detail service start')
        cursor = kwargs['cursor']
        # ログイン情報を取得
        login = super().getLogin(cursor, request)
        userId = login['id']

        # 更新前のチケット情報を取得
        tReq = request.json['body']
        tid = int(tReq['id'])
        tDao = super().dao_manager.get_dao('ticketDao')
        prev = tDao.findTicket(cursor, {'tid': tid})

        # チケット履歴にコピー
        hDao = super().dao_manager.get_dao('ticketHistoryDao')
        hDao.addHistory(cursor, {'tid': tid})

        # チケット更新
        tReq['updateUserId'] = userId
        _Log.debug('ticket update : ' + str(tReq))
        tDao.updateTicket(cursor, tReq)

        # 更新後のチケット情報を取得
        aftr = tDao.findTicket(cursor, {'tid': tid})

        # 更新内容を編集
        memo = self._makeDiff(prev, aftr)
        # 更新内容を履歴に登録
        mDao = super().dao_manager.get_dao('ticketMemoDao')
        r = mDao.findMaxId(cursor, {'tid': tid})
        maxId = (r['max_id'] if r['max_id'] is not None else 0) + 1
        rec = {'id': maxId, 'ticket_id': tid, 'memo': memo,
            'root_memo_id': maxId, 'parent_memo_id': maxId,
            'createUserId': userId}
        mDao.addMemo(cursor, rec)

        # レスポンスの編集
        return {'status': 'OK'}

#[EOF]