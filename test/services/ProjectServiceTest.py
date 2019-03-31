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

if __name__ == '__main__':
    unittest.main()

#[EOF]