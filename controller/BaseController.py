# -*- coding:utf-8 -*-

class BaseController:
    '''
    コントローラクラスの基本クラス
    '''
    def __init__(self, controller_name, mapping):
        self._controller_name = controller_name
        self._mapping = mapping
    @property
    def controller_name(self):
        return self._controller_name
    def execute_post(self, request):
        raise Exception('クラスの継承を行って、execute_postをoverrideして下さい.')
    def set_service_map(self, map):
        self._service_map = map
    def get_service(self, key):
        return self._service_map[key]
    def hasMapping(self, path):
        for map in self._mapping:
            if map['url'] == path:
                return map['method']
        return None
#[EOF]
