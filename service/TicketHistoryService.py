import json
from logging import getLogger
from service.BaseService import BaseService

import util.DBAccess as DBA

_Log = getLogger(__name__)

class TicketHistoryService(BaseService):
    def __init__(self):
        super().__init__('ticketHistory')

    @DBA.Transactional
    def findTicketHistory(self, request, *args, **kwargs):
        '''
        チケット履歴一覧の取得
        '''
        _Log.debug('findTicketHistory service start')
        cursor = kwargs['cursor']
        # 履歴の検索
        dao = super().dao_manager.get_dao('ticketMemoDao')
        p = {'tid': int(request.json['body']['id'])}
        r = dao.findHistory(cursor, p)
        # レスポンスの編集
        if r:
            if not isinstance(r, list):
                r = [r]
            for rec in r:
                rec['create_date'] = super().strfdate(rec['create_date'])
        return r

#[EOF]