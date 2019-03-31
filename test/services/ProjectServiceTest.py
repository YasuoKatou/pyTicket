import sys
sys.dont_write_bytecode = True

from pathlib import Path
#このテストスクリプトからプロジェクトのルートフォルダを検索対象にする
sys.path.append(str(Path(__file__).parent.parent.parent))

import unittest

from pyTicketWeb import make_service_map

class ProjectServiceTest(unittest.TestCase):
    def setUp(self):
        print('start setUp')
        if not hasattr(self, 'ticket_service_map'):
            self.ticket_service_map = make_service_map()
            print('init service map')

    def test_newProjet(self):
        '''
        新規プロジェクトの登録を確認する
        '''
        # サービスを取得する
        service = self.ticket_service_map['project']
        # テスト対象メソッドを呼び出す
        req = {'header': {'app_name': 'ticket tester', 'app_ver': '1.0.0', 'session_id': None},
        'body': {'name': 'テストプロジェクト', 'description': 'プロジェクトの説明', 'manager_id': 1,
        'opened': 'yes', 'alive': 'yes'}}
        ret = service.newProjet(req)
        # 戻り値を確認
        self.assertIsNotNone(ret)               # return is Not None
        self.assertIsInstance(ret, dict)        # return is dictionally
        self.assertEqual('OK', ret['status'])   # 'status' = 'OK'
        self.assertIsNotNone(ret['id'])         # has 'id'
        print('project id : ' + str(ret['id']))

    def test_updateProjet(self):
        '''
        プロジェクトの更新を確認する
        '''
        req_header = {'app_name': 'ticket tester', 'app_ver': '1.0.0', 'session_id': None}
        # サービスを取得する
        service = self.ticket_service_map['project']
        # 更新前データの登録
        req = {'header': req_header,
        'body': {'name': 'テスト', 'description': '説明', 'manager_id': 1,
        'opened': 'yes', 'alive': 'yes'}}
        ret = service.newProjet(req)
        pid = ret['id']
        print('project id : ' + str(pid))
        # データ更新
        req = {'header': req_header,
        'body': {'name': 'テストプロジェクト', 'description': 'プロジェクトの説明', 'manager_id': 2,
        'opened': 'n', 'alive': 'no', 'id': pid}}
        ret = service.updateProjet(req)
        # 戻り値を確認
        self.assertIsNotNone(ret)               # return is Not None
        self.assertIsInstance(ret, dict)        # return is dictionally
        self.assertEqual('OK', ret['status'])   # 'status' = 'OK'
        # 更新データを取得
        find_req = {'header': req_header,
        'body': {'id': pid}}
        ret = service.findProject(find_req)
        # 更新内容を確認する
        prj = ret['project']
        #print(prj)
        self.assertEqual(pid, prj['id'])                    # プロジェクトID
        self.assertEqual('テストプロジェクト', prj['name'])
        self.assertEqual('プロジェクトの説明', prj['description'])
        self.assertEqual(2, prj['manager_id'])
        self.assertEqual('n', prj['opened'])
        self.assertEqual('no', prj['alive'])
        self.assertEqual(2, prj['version_no'])

if __name__ == '__main__':
    unittest.main()

#[EOF]