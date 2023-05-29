import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

from src.settings import ENCRYPTION_CLIENT_KEY, ENCRYPTION_SERVER_KEY


def encrypt(raw, encrypt_key=ENCRYPTION_SERVER_KEY.replace('34', 'ww')):
    raw = pad(raw.encode(), 16)
    encrypt_key = encrypt_key.encode('utf-8')
    cipher = AES.new(encrypt_key, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(raw))

def decrypt(enc, decrypt_key=ENCRYPTION_CLIENT_KEY.replace('34', 'xx')):
    enc = base64.b64decode(enc)
    decrypt_key = decrypt_key.encode('utf-8')
    cipher = AES.new(decrypt_key, AES.MODE_ECB)
    return unpad(cipher.decrypt(enc), 16)
