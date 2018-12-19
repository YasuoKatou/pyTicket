# -*- coding:utf-8 -*-

from bottle import HTTPResponse

class BaseController:
    '''
    コントローラクラスの基本クラス
    '''
    def __init__(self, mapperName):
        self._mapper_name = mapperName;
    @property
    def mapper_name(self):
        return self._mapper_name
    def execute_post(self, request):
        raise Exception('クラスの継承を行って、execute_postをoverrideして下さい.')
    def set_service_map(self, map):
        self._service_map = map
    def get_service(self, key):
        return self._service_map[key]
    def edit_response(self, body):
        r = HTTPResponse(status=200, body=body)
        r.set_header('Content-Type', 'application/json')
        return r
#[EOF]