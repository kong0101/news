from common import cache_


def send_code(email):
    pass


def valid_code(email, code):
    #1.从缓存中读取code(发送的code)
    code_cache = cache_.get_code(email)
    #2.判断缓存中code和用户输入的code是否一致
    print(email, code_cache, code)
    return code_cache == code

