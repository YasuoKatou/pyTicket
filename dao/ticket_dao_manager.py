# -*- coding:utf-8 -*-
from pathlib import Path

from dao.dao_util import get_dao

class TicketDaoManager:
    '''
    各種Daoのインスタンスを保持するクラス
    シングルトンクラスのため「get_instance」メソッドで
    インスタンスを取得すること
    尚、本クラスはマルチスレッドの考慮を行っていない
    参考URL：http://www.denzow.me/entry/2018/01/28/171416
    '''
    _my_self = None
    def __new__(cls):
        raise NotImplementedError('Cannot initialize via Constructor')
    @classmethod
    def __internal_new__(cls):
        cls._dao_map = {}
        #このモジュールと同じフォルダに存在する全xmlファイルを対象にする
        p = Path(__file__).parent
        for xml in p.glob('*.xml'):
            dao = get_dao(xml)
            cls._dao_map[dao.dao_name] = dao
        return super().__new__(cls)
    @classmethod
    def get_instance(cls):
        if not cls._my_self:
            cls._my_self = cls.__internal_new__()
        return cls._my_self

    def get_dao(self, dao_name):
        name = dao_name.lower()
        if name in self._dao_map:
            return self._dao_map[name]
        else:
            return None

#[EOF]