import sys
sys.dont_write_bytecode = True

from pathlib import Path
#このテストスクリプトからプロジェクトのルートフォルダを検索対象にする
sys.path.append(str(Path(__file__).parent.parent.parent))

import unittest

from pyTicketWeb import make_service_map
from util.MyHash import make_hash
from util.MyEncryption import encryption

class LoginServiceTest(unittest.TestCase):
    def setUp(self):
        print('start setUp')
        if not hasattr(self, 'ticket_service_map'):
            self.ticket_service_map = make_service_map()
            print('init service map')
    def test_prepareLogin(self):
        '''
        ログイン準備のテストを行う
        '''
        #ログイン準備を行うサービスを取得
        service = self.ticket_service_map['login']
        #ログイン準備メソッドを呼び出す
        req = {"header": {"app_name": "ticket client", "app_ver": "1.0.0", "session_id": None},
               "body": None}
        ret = service.prepareLogin(req)
        # 戻り値を確認
        self.assertIsNotNone(ret)            # return is Not None
        self.assertIsInstance(ret, dict)     # return is dictionally
        self.assertIn('session_id', ret)     # has 'session_id'
        self.assertEqual(len(ret['session_id']), 64)    # session_id length is 64

    def test_login_01(self):
        '''
        ログインのテストを行う
        '''
        #ログインIDとパスワードのハッシュ化および暗号化
        h_lid = make_hash(u'ykTicket', 'admin')
        h_pwd = make_hash(h_lid, 'admin')
        #ログイン準備／ログインを行うサービスを取得
        service = self.ticket_service_map['login']
        #ログイン準備メソッドを呼び出す
        req = {"header": {"app_name": "ticket client", "app_ver": "1.0.0", "session_id": None},
               "body": None}
        ret = service.prepareLogin(req)
        #ログインメソッドの引数を作成
        sid = ret['session_id']
        req['header']['session_id'] = sid
        key = sid[:16]
        # print('login id : ' + h_lid)
        req['body'] = {"login_id":encryption(key, h_lid).hex() , "passwd":encryption(key, h_pwd).hex()}
        #ログインメソッド呼び出し
        ret = service.doLogin(req)
        # 戻り値を確認
        self.assertIsNotNone(ret)            # return is Not None
        self.assertIsInstance(ret, dict)     # return is dictionally
        self.assertIn('session_id', ret)     # has 'session_id'
        self.assertEqual(len(ret['session_id']), 64)    # session_id length is 64

if __name__ == '__main__':
    unittest.main()

#[EOF]