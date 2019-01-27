# -*- coding:utf-8 -*-

from Crypto.Cipher import AES

def encryption(key, data):
	crypto = AES.new(key.encode('utf-8'))
	return crypto.encrypt(data.encode('utf-8'))


def decryption(key, data):
	crypto = AES.new(key.encode('utf-8'))
	if isinstance(data, bytes):
		return crypto.decrypt(data).decode('utf-8')
	else:
		return crypto.decrypt(bytes.fromhex(data)).decode('utf-8')

if __name__ == '__main__':
	key = '1234567890abcdef'
	data = 'hello Crypto.Cipher AES!       ;'
	print('source    : [' + data + "]")
	#----------------------------------
	#暗号化
	encrypted = encryption(key, data)
	enc_hex = encrypted.hex()

	#----------------------------------
	#復号化
	enc = bytes.fromhex(enc_hex)
	decrypted = decryption(key, enc)
	print('decrypted : [' + decrypted + ']')
#[EOF]