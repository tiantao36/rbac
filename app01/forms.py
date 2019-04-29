from django.forms import Form
from django.forms import fields
from django.forms import widgets
from app01 import models
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

'''
表单验证
'''
class LoginForm(Form):
    username = fields.CharField(required=True,error_messages={'required': "用户名不能为空"},widget=widgets.TextInput(attrs={'class': 'form-control','id':'username','placeholder':"请输入用户","autocomplete":"off"}))
    password = fields.CharField(required=True,error_messages={'required': "密码不能为空"},widget=widgets.TextInput(attrs={'class': 'form-control','id':'password','placeholder':"请输入密码",'type':'password',"autocomplete":"off"}))
    code = fields.CharField(required=True,min_length=5,max_length=5,error_messages={'required': "验证码不能为空",'min_length':'验证码长度5位'},widget=widgets.TextInput(attrs={'class': 'form-control','id':'code','placeholder':"请输入验证码",'type':'text',"autocomplete":"off",'style':"width: 126px;display: inline-block;"}))



class ChangepassForm(Form):
    changpassword_1 = fields.CharField(required=True,min_length=6,error_messages={'required': "密码不能为空","min_length":"至少6位密码"},widget=widgets.TextInput(attrs={'class': 'form-control','id':'changpassword_1','placeholder':"Password",'type':'password','name':'changpassword_1'}))
    changpassword_2 = fields.CharField(required=True,min_length=6,error_messages={'required': "密码不能为空","min_length":"至少6位密码"},widget=widgets.TextInput(attrs={'class': 'form-control','id':'changpassword_2','placeholder':"Password",'type':'password','name':'changpassword_2'}))

    def clean(self):
        changpassword_1 = self.cleaned_data.get('changpassword_1',None)
        changpassword_2 = self.cleaned_data.get('changpassword_2',None)
        if changpassword_1 == changpassword_2:
            return self.cleaned_data
        elif not changpassword_1:
            from django.core.exceptions import ValidationError
            self.add_error('changpassword_1', ValidationError('密码不能为空'))
        elif not changpassword_2:
            from django.core.exceptions import ValidationError
            self.add_error('changpassword_2', ValidationError('密码不能为空'))
        else:
            from django.core.exceptions import ValidationError
            # self.add_error('pwd', ValidationError('密码输入不一致'))
            self.add_error('changpassword_1', ValidationError('密码输入不一致'))
            self.add_error('changpassword_2', ValidationError('密码输入不一致'))
        return self.cleaned_data

