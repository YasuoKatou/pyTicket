# -*- coding:utf-8 -*-

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
#[EOF]