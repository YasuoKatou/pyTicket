# -*- coding:utf-8 -*-

import json
from bottle import HTTPResponse

from controller.BaseController import BaseController

class ProjectController(BaseController):
    '''
    プロジェクトコントローラクラス
    '''
    def __init__(self):
        '''
        URLのマッピングを設定
        '''
        mapping = [
            # プロジェクトの登録
            {'url': '/new_project', 'method': 'newProject'},
            # プロジェクトの更新
            {'url': '/edit_project', 'method': 'editProject'},
            # プロジェクト一覧の取得
            {'url': '/project_list', 'method': 'projectList'}]
        super().__init__('project', mapping)

    def newProject(self, request):
        pass

    def editProject(self, request):
        pass

    def projectList(self, request):
        # ログインサービスを取得
        svc = super().get_service('project')
        # 一覧取得サービスを呼び出し、クライアントに返信する
        return svc.projectList()

#[EOF]