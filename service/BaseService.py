# -*- coding:utf-8 -*-
from logging import getLogger
from datetime import datetime, date

from config.ap_config import Products

_Log = getLogger(__name__)

class BaseService:
    '''
    サービスクラスの基本クラス
    '''
    def __init__(self, service_name):
        self._dao_manager = None
        self._service_name = service_name;

    @property
    def service_name(self):
        return self._service_name

    @property
    def dao_manager(self):
        return self._dao_manager

    @dao_manager.setter
    def dao_manager(self, dao_manager):
        self._dao_manager = dao_manager

    def strftime(self, dt):
        if isinstance(dt, datetime):
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return None

    def strfdate(self, dt):
        if isinstance(dt, date):
            return dt.strftime('%Y-%m-%d')
        else:
            return None

    def getLogin(self, cur, request):
        if 'header' not in request:
            if Products:
                raise Exception('no request header')
            else:
                return {'id': 1}

        dao = self.dao_manager.get_dao('userMasterDao')
        header = request['header']
        if 'session_id' in header and header['session_id'] is not None:
            return dao.findBySessionId(cur, {'session_id': header['session_id']})
        else:
            _Log.info('no session id in header')
            return dao.findById(cur, {'id': 1})

#[EOF]