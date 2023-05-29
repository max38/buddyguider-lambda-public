import json
from src.shared.encryption import encrypt, decrypt
from src.settings import ENCRYPTION_SERVER_KEY


def test_encryption_decryption():
    data = json.dumps({"test": "test"})

    encrypt_key = ENCRYPTION_SERVER_KEY.replace('34', 'ww')

    encrypted = encrypt(data, encrypt_key)
    print('encrypted ECB Base64:',encrypted.decode("utf-8", "ignore"))

    decrypted = decrypt(encrypted, encrypt_key)
    decrypted_data = decrypted.decode("utf-8", "ignore")
    print('data: ', decrypted_data)

    # decrypted_json = json.loads(decrypted_data)
    # print(decrypted_json)
