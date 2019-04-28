# -*- coding:utf-8 -*-

import json
from logging import getLogger
from service.BaseService import BaseService

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
        pid = maxId + 1
        pinfo = request.json['body']
        pinfo['id'] = pid
        pinfo['createUserId'] = login['id']
        dao.addProject(cursor, pinfo)
        # ステータスの初期設定
        p = {'pid': pid, 'createUserId': login['id']}
        dao = super().dao_manager.get_dao('ticketStatusDao')
        dao.copyStatus(cursor, p)
        # 進捗の初期設定
        dao = super().dao_manager.get_dao('ticketProgressDao')
        dao.copyProgress(cursor, p)
        # 種類の初期設定
        dao = super().dao_manager.get_dao('ticketKindDao')
        dao.copyKind(cursor, p)
        # 優先順位の初期設定
        dao = super().dao_manager.get_dao('ticketPriorityDao')
        dao.copyPriority(cursor, p)
        # レスポンスの編集
        return {'status': 'OK'}

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
        pinfo = request.json['body']
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
        p = {'id': int(request.json['body']['project_id'])}
        r = dao.findByProjectId(cursor, p)
        # レスポンスの編集
        r['last_update'] = super().strftime(r['last_update'])
        return r

    def _editProjectList(self, recs):
        '''
        プロジェクト一覧を作成する
        １プロジェクト、複数の種類で構成する
        '''
        r = []
        for rec in recs:
            t_rec = None
            # プロジェクトIDを検索
            for r_rec in r:
                if r_rec['id'] == rec['id']:
                    t_rec = r_rec
                    break
            if t_rec:
                # 同じプロジェクトが存在する場合、種類情報を追加する
                t_rec['kinds'].append({'id': rec['kid'], 'name': rec['kname'],
                    'finish': rec['finish_num'], 'total': rec['total_num']})
            else:
                # プロジェクトが見つからないとき
                r.append({'id': rec['id'],
                    'name': rec['name'],
                    'finish': rec['finish_num'], 'total': rec['total_num'], 
                    'kinds': []
                })
        return r

    @DBA.Transactional
    def projectList(self, *args, **kwargs):
        '''
        プロジェクトの一覧を取得する
        '''
        _Log.debug('projet list service start')
        cursor = kwargs['cursor']
        # 一覧を取得
        dao = super().dao_manager.get_dao('projectDao')
        r = dao.projectList(cursor, {})     # TODO 空の引数を排除したい
        if r:
            return self._editProjectList(r)
        else:
            return None

#[EOF]