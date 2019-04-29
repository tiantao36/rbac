#!/usr/bin/env python
#-*- coding:utf-8 -*-
#http://www.cnblogs.com/wupeiqi/articles/5702910.html
from django.shortcuts import render,HttpResponse,redirect
from django.utils.safestring import mark_safe
from app01.forms import LoginForm
from app01.forms import ChangepassForm
from app01 import models
import json
from django.conf import settings
import re
from app01.utils import createcode
from app01.utils import encrypt

def code(request):
    if request.session.get('code',None):
        del request.session['code']
    imgdata, code = createcode.gene_code()
    request.session['code'] = code
    result=HttpResponse(imgdata,content_type="image/png")
    return result

def login(request):
    if request.method == "GET":
        request.session.flush()  # 强制每次访问都删除登录信息。
        loginform = LoginForm()
        imgdata, code=createcode.gene_code()
        request.session['code']=code
        return render(request, 'base/login.html', {'loginform':loginform,'imgdata':imgdata})
    else:
        loginform = LoginForm(data=request.POST)
        message = {'status': False, 'msg': '','code':False}
        if loginform.is_valid():
            code=loginform.cleaned_data.pop('code').lower()
            scode=request.session.get('code',None).lower()
            loginform.cleaned_data['password']=encrypt.encrypt(loginform.cleaned_data.pop('password'))
            print(loginform.cleaned_data)
            if scode and code==scode:
                message['code']=True
            else:
                from django.core.exceptions import ValidationError
                loginform.add_error("code", ValidationError('验证码错误'))
            user = models.UserInfo.objects.filter(**loginform.cleaned_data).first()
            if user:
                permission_list=models.UserInfo.objects.filter(**loginform.cleaned_data).values(
                    'roles__permissions__id',
                    'roles__permissions__title', #
                    'roles__permissions__url',
                    'roles__permissions__is_menu', #
                    'roles__permissions__parent_id', # 当前权限所在组，的菜单ID
                    'roles__permissions__imgurl', # 当前权限所在组，的菜单ID
                ).distinct()
                #根据每个用户生成菜单
                page_menu = {}
                # 防止访问没有权限的url
                permission_url = []
                basepermission_url=models.Basepermission.objects.values('url')
                for urlobj in basepermission_url:
                    permission_url.append(urlobj.get('url'))


                '''
              {
                1: {'url': '/ttest/', 'title': '测试管理', 'imgurl': 'test_fill.png', 'children': [{'title': '环境管理', 'url': '/ttest/env/'},]
              }
              '''

                for item in permission_list:
                    is_menu = item['roles__permissions__is_menu']
                    title= item['roles__permissions__title']
                    url=item['roles__permissions__url']
                    imgurl=item['roles__permissions__imgurl']
                    menu_id=item['roles__permissions__id']
                    parent_id=item['roles__permissions__parent_id']
                    if not is_menu:
                        continue
                    permission_url.append(url)
                    if not parent_id:
                        page_menu[menu_id] = {'title': title,'imgurl':imgurl,'url': url,'children': []}
                    else:
                        child = {'title': title, 'url': url}
                        page_menu[parent_id]['children'].append(child)


                print(page_menu)
                print(permission_url)
                print(user.username)
                request.session['page_menu']=page_menu
                request.session['username']=user.username
                request.session['permission_url']=permission_url
                message['status'] = True
            else:
                # 用户验证失败返回报错
                from django.core.exceptions import ValidationError
                loginform.add_error("username", ValidationError('用户名或密码错误'))
                loginform.add_error("password", ValidationError('用户名或密码错误'))
                code = loginform.cleaned_data.get('code', None)
            if code:
                code = code.lower()
                scode = request.session.get('code', None).lower()
                if scode and code == scode:
                    message['code'] = True
                else:
                    from django.core.exceptions import ValidationError
                    loginform.add_error("code", ValidationError('验证码错误'))
        else:
            # 表单from规则验证失败处理
            from django.core.exceptions import ValidationError
            # loginform.add_error("username", ValidationError('用户名或密码错误'))
            # loginform.add_error("password", ValidationError('用户名或密码错误'))
            code = loginform.cleaned_data.get('code',None)
            if code:
                code = code.lower()
                scode = request.session.get('code', None).lower()
                if scode and code == scode:
                    message['code'] = True
                else:
                    from django.core.exceptions import ValidationError
                    loginform.add_error("code", ValidationError('验证码错误'))
        message['msg'] = loginform.errors
        return HttpResponse(json.dumps(message))


def index(request):
    page_menu=request.session['page_menu']
    return render(request, 'base/index.html', context={'page_menu':page_menu})


def llog(request):
    from django.conf import settings
    import os
    path=r'{0}'.format(__file__)
    with open(path,encoding='utf-8') as f:
        result=f.read()
    html='''<pre>{0}</pre>'''.format(result)
    data={'data':mark_safe(html)}
    return HttpResponse(json.dumps(data))

def logout(request):
    request.session.flush()
    return redirect('/')

def changepass(request):
    print('######################')
    changepassform=ChangepassForm(data=request.POST)
    username=request.session.get('username')
    message={'status':False,'msg':''}
    if changepassform.is_valid():
        password=changepassform.cleaned_data['changpassword_1']
        models.UserInfo.objects.filter(username=username).update(password=encrypt.encrypt(password))
        message['status']=True
        return HttpResponse(json.dumps(message, ensure_ascii=False))
    else:
        message['msg']=changepassform.errors
        print(message)
        return HttpResponse(json.dumps(message,ensure_ascii=False))