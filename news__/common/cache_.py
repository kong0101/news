from common import rd

def save_code(phone,code):
    rd.set(phone, code, ex=60) #两分钟有效时间


def get_code(phone):
    return rd.get(phone)


def add_token(token, user_id):
    rd.set(token,user_id, ex=3600 * 24 * 7)


def get_user_id(token):
    # API接口操作时，需要通过接口中token参数获取登录的用户信息
    return rd.get(token)

def del_token(token):
    #退出登陆删除缓存中的token
    rd.delete(token)

