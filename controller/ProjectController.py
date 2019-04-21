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
            {'url': '/project_list', 'method': 'projectList'},
            # プロジェクト詳細の取得
            {'url': '/project_detail', 'method': 'projectDetail'}]
        super().__init__('project', mapping)

    def newProject(self, request):
        '''
        プロジェクトの新規登録
        '''
        # プロジェクトサービスを取得
        svc = super().get_service('project')
        # プロジェクトを登録し、
        svc_result = svc.newProjet(request)
        # 登録結果をクライアントに返信する
        if svc_result['status'] == 'OK':
            return super().editOKResponse(None)
        else:
            return super().editNGResponse(svc_result['reason'])

    def editProject(self, request):
        '''
        プロジェクトの更新
        '''
        # プロジェクトサービスを取得
        svc = super().get_service('project')
        # プロジェクトを更新し、更新結果をクライアントに返信する
        svc_result = svc.updateProjet(request)
        if svc_result['status'] == 'OK':
            return super().editOKResponse(None)
        else:
            return super().editNGResponse(svc_result['reason'])

    def projectList(self, request):
        '''
        プロジェクト一覧の取得
        '''
        # プロジェクトサービスを取得
        svc = super().get_service('project')
        # 一覧取得サービスを呼び出し、
        svc_data = svc.projectList()
        # 一覧をクライアントに返信する
        return super().editOKResponse(svc_data)

    def projectDetail(self, request):
        '''
        プロジェクトの詳細取得
        '''
        # プロジェクトサービスを取得
        svc = super().get_service('project')
        # 詳細取得サービスを呼び出し、
        svc_data = svc.findProject(request)
        # 詳細情報をクライアントに返信する
        return super().editOKResponse(svc_data)

#[EOF]