import json

from django.http import HttpResponse

from common import md5_, token_, cache_, code_
from mainapp.models import TUser


# 发送验证码
def get_code(request):
    email = request.POST['email'].strip()
    if email:
        code_.send_code(email)
        info = {'state': 0, 'msg': '验证码已发送'}
    else:
        info = {'state': 1, 'msg': '邮箱不能为空'}
    return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')


# 注册
def register(request):
    email = request.POST['email'].strip()
    vaild_code = request.POST['vaild'].strip()
    if not all((email, vaild_code)):
        info = {'state': 1, 'msg': '用户名或验证码不能为空！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    if not code_.valid_code(email, vaild_code):
        info = {'state': 1, 'msg': '验证码输入错误！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    # if vaild_code != '0000':
    #     info = {'state': 1, 'msg': '验证码输入错误！'}
    #     return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    user = TUser()
    user.email = email
    token = token_.gen_token(user.user_id)
    user.save()
    print(token, user.email)
    cache_.add_token(token, user.user_id)
    head_url = 'http://localhost:8000/static/天空.jpg'
    nickname = '昵称'
    info = {'state': 0, 'msg': '登录成功！', 'token': token, 'head_url': head_url, 'nickname': nickname}
    return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')


# 验证码登录
def login_vaild(request):
    email = request.POST['email'].strip()
    vaild_code = request.POST['vaild'].strip()

    if not all((email, vaild_code)):
        info = {'state': 1, 'msg': '用户名或验证码不能为空！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    if not code_.valid_code(email, vaild_code):
        info = {'state': 1, 'msg': '验证码输入错误！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    login_user = TUser.objects.filter(email=email).first()
    if login_user:
        token = token_.gen_token(login_user.user_id)
        cache_.add_token(token, login_user.user_id)
        head_url = 'http://localhost:8000/static/天空.jpg'
        if login_user.img:
            head_url = login_user.img
        nickname = '昵称'
        if login_user.nickname:
            nickname = login_user.nickname
        info = {'state': 0, 'msg': '登录成功！', 'token': token, 'head_url': head_url, 'nickname': nickname}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    else:
        info = {'state': 1, 'msg': '该用户未注册！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')


# 账号密码登录
def login_pwd(request):
    email = request.POST['email'].strip()
    password = request.POST['password'].strip()
    if not all((email, password)):
        info = {'state': 1, 'msg': '用户名或口令不能为空！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    password_ = md5_.hash_encode(password)
    login_user = TUser.objects.filter(email=email, password=password_).first()
    if login_user:
        token = token_.gen_token(login_user.user_id)
        cache_.add_token(token, login_user.user_id)
        head_url = 'http://localhost:8000/static/天空.jpg'
        if login_user.img:
            head_url = login_user.img
        nickname = '昵称'
        if login_user.nickname:
            nickname = login_user.nickname
        info = {'state': 0, 'msg': '登录成功！', 'token': token, 'head_url': head_url, 'nickname': nickname}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    else:
        info = {'state': 1, 'msg': '用户名或口令错误！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')


# 注销登录
def logout(request):
    token = request.POST['token'].strip()
    cache_.del_token(token)
    info = {'state': 0, 'msg': '退出登录成功！'}
    return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')


# 设置密码
def set_pwd(request):
    token = request.POST['token'].strip()
    password = request.POST['password'].strip()
    password_ = request.POST['password_'].strip()
    if password != password_:
        info = {'state': 1, 'msg': '密码不一致！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    id_ = cache_.get_user_id(token)
    print(token, id_)
    user = TUser.objects.get(pk=id_)
    pwd = md5_.hash_encode(password)
    user.password = pwd
    user.save()
    info = {'state': 0, 'msg': '密码设置成功！'}
    return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')


# 修改密码
def change_pwd(request):
    token = request.POST['token'].strip()
    password = request.POST['password'].strip()
    password_ = request.POST['password_'].strip()
    password__ = request.POST['password__'].strip()
    id_ = cache_.get_user_id(token)
    user = TUser.objects.get(pk=id_)
    if password != user.password:
        info = {'state': 1, 'msg': '原密码错误！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    if password_ != password__:
        info = {'state': 1, 'msg': '密码不一致！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    pwd = md5_.hash_encode(password_)
    user.password = pwd
    user.save()
    info = {'state': 0, 'msg': '密码修改成功！'}
    return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')


# 修改个人信息
def change_information(request):
    token = request.POST['token'].strip()
    nickname = request.POST['nickname'].strip()
    sex = request.POST['sex'].strip()
    id_ = cache_.get_user_id(token)
    user = TUser.objects.get(pk=id_)
    if nickname:
        user.nickname = nickname
    if sex:
        user.sex = sex
    user.save()
    info = {'state': 0, 'msg': '个人信息修改成功！'}
    return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')


# 上传头像
def upload_head(request):
    token = request.POST['token'].strip()
    image = request.POST['image'].strip()
    id_ = cache_.get_user_id(token)
    user = TUser.objects.get(pk=id_)
    if image:
        with open(f'heads/{user.user_id}/head_{user.user_id}.jpg', 'wb') as f:
            f.write(image)
        user.img = f'http://localhost:8000/head/{user.user_id}/head_{user.user_id}.jpg'
        user.save()
        info = {'state': 0, 'msg': '头像上传成功！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
    else:
        user.save()
        info = {'state': 1, 'msg': '头像上传失败！'}
        return HttpResponse(json.dumps(info, ensure_ascii=False), content_type='application/json', charset='utf-8')
