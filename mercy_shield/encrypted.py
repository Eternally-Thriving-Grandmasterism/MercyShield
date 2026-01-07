from cryptography.fernet import Fernet
import os

KEY_PATH = "/sdcard/mercy_key.bin"

def get_key():
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, 'rb') as f:
            return f.read()
    key = Fernet.generate_key()
    with open(KEY_PATH, 'wb') as f:
        f.write(key)
    return key

cipher = Fernet(get_key())

def encrypt(data: str) -> str:
    return cipher.encrypt(data.encode()).decode()

def decrypt(data: str) -> str:
    return cipher.decrypt(data.encode()).decode()
