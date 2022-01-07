import os, struct
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from random import randint

def main():
    password = 'kitty'
    password = password.encode()
    h = SHA256.new()
    h.update(password)
    key = h.digest()

    encrypt_file(key, 'calc.exe')
    decrypt_file(key,'calc.exe.enc')


def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    IV = [randint(0, 0xFF) for i in range(16)]
    IV = bytes(IV)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    filesize = os.path.getsize(in_filename)
    
    f_in = open(in_filename, 'rb')
    f_out = open(out_filename, 'wb')
    
    f_out.write(struct.pack('<Q', filesize))
    f_out.write(IV)

    while True:
        chunk = f_in.read(chunksize)
        if len(chunk) == 0:
            break
        elif len(chunk) % 16 != 0:
            chunk += b' ' * (16 - len(chunk) % 16)
        f_out.write(encryptor.encrypt(chunk))
    f_in.close()
    f_out.close()

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = in_filename + '.dec'
    
    f_in = open(in_filename, 'rb')
    f_out = open(out_filename, 'wb')
    filesize = f_in.read(8)
    filesize = struct.unpack('<Q', filesize)[0]
    IV = f_in.read(16)
    decryptor = AES.new(key, AES.MODE_CBC, IV)

    while True:
        chunk = f_in.read(chunksize)
        if len(chunk) == 0:
            break
        f_out.write(decryptor.decrypt(chunk))
        f_out.truncate(filesize)
    f_in.close()
    f_out.close()
    
if __name__ == '__main__':
    main()
