import re

_RE_JOIN = re.compile(r'.*[ )](?i)(and|or)[ (].*')
#四則演算子を判定する正規表現
_RE_ARITH = re.compile(r'[¥+¥*/]|[-]')
#比較演算子を判定する正規表現
_RE_TEST = re.compile(r'==|!=|<=|>=|<|>')
#変数を判定する税期表現
_HEN = re.compile(r'[a-zA-Z_]+.?')

class saBase:
	'''
	演算を行う基本クラス
	'''
	def __init__(self, value):
		self._value = value
	@property
	def value(self):
		return self._value
class saVal(saBase):
	'''
	値を保持するクラス
	'''
	def __init__(self, value):
		if isinstance(value, str):
			super().__init__(value)
			self._num = None
		else:
			super().__init__(str(value))
			self._num = value
	@property
	def number(self):
		return self._num
	@number.setter
	def number(self, num):
		self._num = num
class saHen(saBase):
	'''
	変数を保持するクラス
	※nullやNoneも変数としてこのクラスに保持する
	'''
	def __init__(self, value):
		super().__init__(value)
	def getByName(self, val_disct):
		if self._value.lower() == 'null':
			return None
		elif self._value == 'None':
			return None
		else:
			if self._value in val_disct:
				return val_disct[self._value]
		return None
class saOpe(saBase):
	'''
	四則演算子を保持するクラス
	'''
	def __init__(self, value):
		super().__init__(value)
class saTest(saBase):
	'''
	比較演算子を保持するクラス
	'''
	def __init__(self, value):
		super().__init__(value)
class saBrkr(saBase):
	'''
	括弧を保持するクラス
	'''
	def __init__(self, value):
		super().__init__(value)

def calc(f):
	'''
	四則演算を計算する
	'''
	#乗算と剰余を先に計算
	pf = True
	while pf:
		pf = False
		for idx in range(0, len(f)):
			c = f[idx]
			if isinstance(c, saOpe):
				y = None
				if c.value == '*':
					y = f[idx-1].number * f[idx+1].number
				elif c.value == '/':
					y = f[idx-1].number / f[idx+1].number
				if y:
					f[idx] = saVal(y)
					f.pop(idx+1)
					f.pop(idx-1)
					pf = True if len(f) > 1 else False
					break
	#加算と減算を計算する
	pf = True
	while pf:
		pf = False
		for idx in range(0, len(f)):
			c = f[idx]
			if isinstance(c, saOpe):
				if c.value == '+':
					y = f[idx-1].number + f[idx+1].number
				elif c.value == '-':
					y = f[idx-1].number - f[idx+1].number
				f[idx] = saVal(y)
				f.pop(idx+1)
				f.pop(idx-1)
				pf = True if len(f) > 1 else False
				break
	return f

def condition_check(f, v):
	'''
	条件式(a == b)を判定する
	'''
	for idx in range(0, len(f)):
		c1 = f[idx-1]
		c2 = f[idx]
		c3 = f[idx+1]
		if isinstance(c2, saTest):
			l = c1.getByName(v) if isinstance(c1, saHen) else c1.value
			r = c3.getByName(v) if isinstance(c3, saHen) else c3.value
			try:
				return eval(str(l) + c2.value + str(r))
			except:
				return False
	return False

def makeSyntacClass(l):
	'''
	文字列の計算式または条件式をクラスに割り当てる
	'''
	r = []
	for i in l:
		#四則演算子の確認
		m = re.match(_RE_ARITH, i)
		if m:
			r.append(saOpe(i))
			continue
		#変数の確認
		m = re.match(_HEN, i)
		if m:
			r.append(saHen(i))
			continue
		#数値(整数)の確認
		try:
			x = int(i)
			c = saVal(i)
			c.number = x
			r.append(c)
			continue
		except:
			pass
		#数値(小数)の確認
		try:
			x = float(i)
			c = saVal(i)
			c.number = x
			r.append(c)
			continue
		except:
			pass
		#条件式
		m = re.match(_RE_TEST, i)
		if m:
			r.append(saTest(i))
			continue
		#todo 括弧の判定
	return r

def join_condition(f):
	m = re.match(_RE_JOIN, f)
	#print(m)
	return m

def sep_bracket_level1(f):
	'''
	括弧を分離する
	'''
	pos = f.find('(')
	if pos < 0:
		return [f]

	left = None
	right = None
	if pos > 0:
		#式の途中から括弧が始まる
		left = f[:pos]
	#閉じ括弧を探す
	c = 1
	tail = len(f)
	for p2 in range(pos+1, tail+1):
		s = f[p2:p2+1]
		if s == '(':
			#階層がある括弧
			c += 1
		elif s == ')':
			c -= 1
			if c == 0:
				middle = f[pos+1:p2]
				if p2 < tail:
					#式の途中で括弧が終わる
					right = f[p2+1:]
				break
	r = []
	if left:
		r.append(left.strip())
	r.append(middle.strip())
	if right:
		r.append(right.strip())
	return r

def sep_arithmetic(f):
	''' 
	計算式(文字列)を四則演算子で分離する
	'''
	r = []
	bre = True
	while bre:
		bre = False
		ite = re.finditer(_RE_ARITH, f)
		for m in ite:
			#print(dir(m))
			if m.start() > 0:
				r.append(f[:m.start()].strip())
			r.append(f[m.start():m.end()])
			f = f[m.end():].strip()
			bre = True
			break
	if len(f) > 0:
		r.append(f)
	return r

def sep_test(f):
	'''
	条件式(文字列)を比較演算子で分離する
	'''
	r = []
	ite = re.finditer(_RE_TEST, f)
	for m in ite:
		r.append(f[:m.start()].strip())
		r.append(f[m.start():m.end()])
		r.append(f[m.end():].strip())
	return r

class TestTagExp:
	@staticmethod
	def doTest(f, v):
		#条件式(文字列)を比較演算子で分割
		r = sep_test(f)
		#分離結果から計算クラスを作成
		r = makeSyntacClass(r)
		#判定を行う
		return condition_check(r, v)
'''
if __name__ == '__main__':
	assert TestTagExp.doTest('id == null', {}), '「==」で変数が存在しない'
	assert TestTagExp.doTest('id == null', {'id':None}), '「==」で変数の値が存在不一致'
	assert TestTagExp.doTest('id != null', {}) == False, '「!=」で変数が存在しない'
	assert TestTagExp.doTest('id != null', {'id':None}) == False, '「!=」で変数の値が存在不一致'
	assert TestTagExp.doTest('a1 == b1', {'a1':2, 'b1':2}), '「==」で変数の値が一致'
	assert TestTagExp.doTest('a1 == b1', {'a1':2, 'b1':3}) == False, '「==」で変数の値が不一致'
	assert TestTagExp.doTest('a1 != b1', {'a1':2, 'b1':2}) == False, '「!=」で変数の値が一致'
	assert TestTagExp.doTest('a1 != b1', {'a1':2, 'b1':3}), '「!=」で変数の値が不一致'
	print('Test OK')
'''
#[EOF]