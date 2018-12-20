# -*- coding:utf-8 -*-
import numpy as np

def revert(a, n):
	'''
	文字列aを反転し、長さnを戻す
	'''
	return [int(a[i-1:i]) for i in range(len(a), len(a)-n, -1)]

def TFs(m):
	'''
	指定した要素数の真偽値をランダムに生成する
	'''
	bc = 10
	f = '{:1.' + str(bc) + 'f}'
	c = divmod(m, bc)
	n = c[0]
	if c[1] > 0:
		n += 1
	a = np.random.rand(n)
	s = []
	for b in a:
		w = f.format(b)
		s += w[len(w)-10:len(w)]

	return [True if (int(x) % 2) == 0 else False for x in s]

def rand_n(cols=64):
	br = 4
	bc = 10			#小数点以下10桁を処理する
	f = '{:1.' + str(bc) + 'f}'
	c = divmod(cols, bc)
	mc = c[0]
	if c[1] > 0:
		mc +=1
	# step 1 : 4 * mc の乱数を生成
	w = np.random.normal(1, 10, (br, mc))

	# step 2 : 乱数の小数部を文字列に変換し、
	#					 数字を作成
	s = ['' for x in range(0, br)]
	i = 0
	for r in w:
		for j in range(0, len(r)):
			w = f.format(r[j])
			#print(w)
			s[i] = s[i] + w[len(w)-bc:len(w)]
		i += 1

	# step 3 : 文字を反転させる
	x = []
	for sd in s:
		x.append(revert(sd, len(sd)))

	# step 4 : 文字列を入れ替える
	np.random.shuffle(x)

	# step 5 : 各列を加算
	y1 = [x + y for (x, y) in zip(x[0], x[1])]
	y2 = [x + y for (x, y) in zip(x[2], x[3])]
	y = [x + y for (x, y) in zip(y1, y2)]

	# step 6 : 16進の1桁を連結
	h = ''
	tf = TFs(cols)
	i = 0
	for d in y:
		s = hex(d)
		if tf[i]:
			s = s.upper()
		h += s[len(s)-1:]
		i += 1
	return h[:cols]

if __name__ == '__main__':
	for c in range(1, 50):
		w = rand_n()
		print(len(w), w)
#[EOF]