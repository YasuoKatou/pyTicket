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
        '''
        プロジェクトの新規登録
        '''
        # プロジェクトサービスを取得
        svc = super().get_service('project')
        # プロジェクトを登録し、登録結果をクライアントに返信する
        return svc.newProjet(request)

    def editProject(self, request):
        '''
        プロジェクトの更新
        '''
        # プロジェクトサービスを取得
        svc = super().get_service('project')
        # プロジェクトを更新し、更新結果をクライアントに返信する
        return svc.updateProjet(request)

    def projectList(self, request):
        '''
        プロジェクト一覧の取得
        '''
        # プロジェクトサービスを取得
        svc = super().get_service('project')
        # 一覧取得サービスを呼び出し、クライアントに返信する
        return svc.projectList()

#[EOF]