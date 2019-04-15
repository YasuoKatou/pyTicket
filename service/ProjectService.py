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
        cursor = kwargs['cursor']
        # ログイン情報を取得
        login = super().getLogin(cursor, request)
        # 最大のプロジェクトIDを取得
        dao = super().dao_manager.get_dao('projectDao')
        r = dao.findMaxId(cursor, {})
        maxId = r['max_id'] if r['max_id'] is not None else 0
        _Log.debug('new project id : ' + str(maxId))
        # 新規プロジェクトの登録
        pinfo = request['body']
        pinfo['id'] = maxId + 1
        pinfo['createUserId'] = login['id']
        dao.addProject(cursor, pinfo)
        # レスポンスの編集
        return {'status': 'OK', 'id': pinfo['id']}

    @DBA.Transactional
    def updateProjet(self, request, *args, **kwargs):
        '''
        プロジェクトの更新を行う
        '''
        _Log.debug('update projet service start')
        cursor = kwargs['cursor']
        # ログイン情報を取得
        login = super().getLogin(cursor, request)
        # プロジェクトの更新
        pinfo = request['body']
        pinfo['updateUserId'] = login['id']
        dao = super().dao_manager.get_dao('projectDao')
        dao.updateProject(cursor, pinfo)
        # レスポンスの編集
        return {'status': 'OK'}

    @DBA.Transactional
    def findProject(self, request, *args, **kwargs):
        '''
        プロジェクトの検索を行う
        '''
        _Log.debug('find projet service start')
        cursor = kwargs['cursor']
        # プロジェクトの検索
        dao = super().dao_manager.get_dao('projectDao')
        r = dao.findByProjectId(cursor, request['body'])
        # レスポンスの編集
        return {'status': 'OK', 'project': r}

    @DBA.Transactional
    def projectList(self, *args, **kwargs):
        '''
        プロジェクトの一覧を取得する
        '''
        _Log.debug('projet list service start')
        cursor = kwargs['cursor']
        # 一覧を取得
        dao = super().dao_manager.get_dao('projectDao')
        r = dao.projectList(cursor)
        # レスポンスの編集
        return {'status': 'OK', 'list': r}

#[EOF]