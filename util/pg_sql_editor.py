import re

#SQL内の変数定義
_RE_VALIABLE = re.compile(r'#\{[\w]*\}')

class SqlEditor:
	@staticmethod
	def edit_valiables(source, values=None):
		q = []
		v = []
		sp = 0
		ite = re.finditer(_RE_VALIABLE, source)
		for m in ite:
			#変数より左を取得
			q.append(source[sp:m.start()])
			#変数名#{xxx)を取得
			vn = source[m.start()+2:m.end()-1].strip()
			#print('valiavle name', vn)
			sp = m.end()	#'}'で終わる
			q.append('%s')
			x = values[vn] if vn in values else None
			v.append(x)
		if sp < len(source):
			q.append(source[sp:])
		return ''.join(q), tuple(v)

#[EOF]