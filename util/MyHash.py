import hashlib

def make_hash(*args):
	#print(args)
	m = hashlib.sha256()
	for x in args:
		#print(x)
		m.update(x.encode('utf-8'))
	return m.hexdigest()

if __name__ == '__main__':
	'''
	DBに登録するログインIDとパスワードのハッシュ化
	'''
	#ログインIDのハッシュ化
	uid = u'admin'
	h_lid = make_hash(u'ykTicket', uid)
	print('login id :', h_lid)

	#パスワードのハッシュ化
	pwd = u'admin'
	h_pwd = make_hash(h_lid, pwd)
	print('passwd :', h_pwd)

#[EOF]