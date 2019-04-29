from django.template import Library
from django.conf import settings
from app01.forms import ChangepassForm
from app01 import models
import re
register = Library()
'''
生成菜单页
'''
@register.inclusion_tag('base/menu_tpl.html')
def menu_html(request):
    page_menu=request.session['page_menu']
    return {'page_menu':page_menu}


@register.inclusion_tag('base/changepass_tpl.html')
def changepass_html(request):
    changepassform=ChangepassForm()
    return {'changepassform': changepassform}