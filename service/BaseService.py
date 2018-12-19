# -*- coding:utf-8 -*-

class BaseService:
    '''
    サービスクラスの基本クラス
    '''
    def __init__(self, mapperName):
        self._mapper_name = mapperName;
    @property
    def mapper_name(self):
        return self._mapper_name
#[EOF]