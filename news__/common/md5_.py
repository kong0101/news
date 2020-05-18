import hashlib
from news.settings import SECRET_KEY


def hash_encode(txt, secret_sign=SECRET_KEY):
    auth_m = hashlib.md5(txt.encode('utf-8'))
    auth_m.update(secret_sign.encode('utf-8'))
    return auth_m.hexdigest()
