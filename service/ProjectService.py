# -*- coding:utf-8 -*-

import json
from logging import getLogger
from service.BaseService import BaseService

from util.MyRandom import rand_n
from util.MyEncryption import decryption

import util.DBAccess as DBA

_Log = getLogger(__name__)

class ProjectService(BaseService):
    def __init__(self):
        super().__init__('project')

    @DBA.Transactional
    def newProjet(self, request, *args, **kwargs):
        '''
        プロジェクトの新規登録を行う
        '''
        _Log.debug('new projet service start')
        dao = super().dao_manager.get_dao('projectDao')
        # 最大のプロジェクトIDを取得
        maxId = dao.findMaxId()
        if not maxId:
            maxId = 0
        _Log.debug('new project id : ' + maxId)
        # 新規プロジェクトの登録
        pinfo = request['body']
        pinfo['id'] = maxId + 1
        cnt = dao.addProject(pinfo)
        if cnt != 1:
            raise Exception('DB error : 新規プロジェクト登録エラー')
        # レスポンスの編集
        return {'status': 'OK', 'id': maxId}

    @DBA.Transactional
    def updateProjet(self, request, *args, **kwargs):
        '''
        プロジェクトの更新を行う
        '''
        _Log.debug('update projet service start')
        # TODO プロジェクトの更新
        # TODO レスポンスの編集

#[EOF]