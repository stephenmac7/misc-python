from Crypto.Cipher import AES
from Crypto import Random

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

def encrypt(text, key):
    """ Encrypts text with AES using key """
    iv = Random.new().read(BS)
    cipher = AES.new(pad(key), AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(text))

def decrypt(text, key):
    """ Decrypts text with AES using key """
    iv = text[:BS]
    enc = text[BS:]
    cipher = AES.new(pad(key), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc).decode())

if __name__ == "__main__":
    key = "somekey"
    test = input("Input: ")
    print(decrypt(encrypt(test, key), key))
