from Crypto.Cipher import AES

def encryption(key, data):
	crypto = AES.new(key.encode('utf-8'))
	return crypto.encrypt(data.encode('utf-8'))


def decryption(key, data):
	crypto = AES.new(key.encode('utf-8'))
	return crypto.decrypt(data).decode('utf-8')

if __name__ == '__main__':
	key = '1234567890abcdef'
	data = 'hello Crypto.Cipher AES!       ;'
	print('source    : [' + data + "]")
	#
	encrypted = encryption(key, data)
	#print('type of encrypted', type(encrypted))
	enc_hex = encrypted.hex()
	#print('encrypted', enc_hex)

	#
	dec = bytes.fromhex(enc_hex)
	#print(dec)
	decrypted = decryption(key, dec)
	print('decrypted : [' + decrypted + ']')
#[EOF]
