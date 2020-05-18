import json


from common import md5_, token_, cache_, code_
from mainapp.models import TUser


def get_code(request):
    email = request.POST['email'].strip()
    if email:
        code_.send_code(email)
        info = {'state': 0, 'msg': '验证码已发送'}
    else:
        info = {'state': 1, 'msg': '邮箱不能为空'}
    return json.dumps(info)


def register(request):
    email = request.POST['email'].strip()
    vaild_code = request.POST['vaild'].strip()
    if not all((email, vaild_code)):
        info = {'state': 1, 'msg': '用户名或验证码不能为空！'}
        return json.dumps(info)
    if not code_.valid_code(email, vaild_code):
        info = {'state': 1, 'msg': '验证码输入错误！'}
        return json.dumps(info)
    user = TUser()
    user.email = email
    token = token_.gen_token(user.user_id)
    cache_.add_token(token, user.user_id)
    if user.img:
        head_url = cache_.get_head_url(user.img)
        if not head_url:
            head_url = '12243'

            cache_.save_head_url(user.img, head_url)
    info = {'state': 0, 'msg': '注册成功', 'token': token}
    return json.dumps(info)


def login_vaild(request):
    email = request.POST['email'].strip()
    vaild_code = request.POST['vaild'].strip()

    if not all((email, vaild_code)):
        login_info = {'state': 1, 'msg': '用户名或验证码不能为空！'}
        return json.dumps(login_info)
    if not code_.valid_code(email, vaild_code):
        login_info = {'state': 1, 'msg': '验证码输入错误！'}
        return json.dumps(login_info)
    login_user = TUser.objects.filter(email=email)
    if login_user:
        token = token_.gen_token(login_user.user_id)
        cache_.add_token(token, login_user.user_id)
        if login_user.img:
            head_url = cache_.get_head_url(login_user.img)
            if not head_url:
                head_url = '12243'
                cache_.save_head_url(login_user.img, head_url)
        login_info = {'state': 0, 'msg': '登录成功！', 'token': token}
        return json.dumps(login_info)
    else:
        login_info = {'state': 1, 'msg': '该用户未注册！'}
        return json.dumps(login_info)


def login_pwd(request):
    email = request.POST['email'].strip()
    password = request.POST['password'].strip()
    if not all((email, password)):
        login_info = {'state': 1, 'msg': '用户名或口令不能为空！'}
        return json.dumps(login_info)
    password_ = md5_.hash_encode(password)
    login_user = TUser.objects.filter(email=email, password=password_)
    if login_user:
        token = token_.gen_token(login_user.user_id)
        cache_.add_token(token, login_user.user_id)
        head_url = 'http://localhost:8000/static/head.jpg'
        if login_user.image:
            head_url = login_user.image
        nickname = '昵称'
        if login_user.nickname:
            nickname = login_user.nickname
        login_info = {'state': 0, 'msg': '登录成功！', 'token': token, 'head_url': head_url, 'nickname': nickname}
        return json.dumps(login_info)
    else:
        login_info = {'state': 1, 'msg': '用户名或口令错误！'}
        return json.dumps(login_info)


def logout(request):
    token = request.GET('token')
    cache_.del_token(token)
    info = {'state': 0, 'msg': '退出登录成功！'}
    return json.dumps(info)
