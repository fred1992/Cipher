from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random._UserFriendlyRNG import get_random_bytes

password = 'kitty'
h = SHA256.new()
h.update(bytes(password, 'utf-8'))
key = h.digest()
print('Key: ',key)

IV = get_random_bytes(16) 
print('IV: ',IV)

mode = AES.MODE_CBC
encryptor = AES.new(key, mode, IV)

plain_text = 'A' * 16
print('Playn text: ', plain_text)

cipher_text = encryptor.encrypt(plain_text)
print('Cipher text: ', cipher_text)

decryptor = AES.new (key, mode, IV=IV)
plain_text1 = decryptor.decrypt (cipher_text)
print('Plain text: ', plain_text1)

