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
from app01.utils import imges_monitor



def index(request):
    '''
        {% for host, hostid, graphid, numt, key, times,item in data %}
            var h1_tag=$('<h1>').html("<span style='color:red;'>{{ times }}</span>--{{ host }}--{{ numt }}")
            $("body div").append(h1_tag);
            var img_tag=$('<img>').attr('src', 'data:image/png;base64,{{ item }}');
            $("body div").append(img_tag);
        {% endfor %}

    :param request:
    :return:
    '''

    # imgdata=imges_monitor.handler()
    # data = {'data_length':len(imgdata)}
    # for host, hostid, graphid, numt, key, times,item in imgdata:
    #     h1_tag ='''<h1 class="page-header" style='color:red;font-size:20px;text-align:center;'>{times}--{host}--{numt}</h1>'''.format(times=times,host=host,numt=numt)
    #     img_tag ='''<img class="img-responsive" style="margin:0 auto;" src="data:image/png;base64,{item}">'''.format(item=re.search("^b'(.*?)'$",str(item)).groups()[0])
    #     data[h1_tag]=img_tag
    #
    # print(request.POST)
    # print(request.body.decode())
    # print(json.loads(request.body.decode()))
    imgdata=imges_monitor.handler()
    data = {'status': False}
    if imgdata:
        data['status']=True
        data['data_length']=len(imgdata)
        data['img']={}
        for host, hostid, graphid, numt, key, times,item in imgdata:
            # print(host, hostid, graphid, numt, key, times,item)
            h1_tag ='''<h1 class="page-header" style='color:red;font-size:20px;text-align:center;'>{times}--{host}--{numt}</h1>'''.format(times=times,host=host,numt=numt)
            img_tag ='''<img class="img-responsive" style="margin:0 auto;" src="data:image/png;base64,{item}">'''.format(item=re.search("^b'(.*?)'$",str(item)).groups()[0])
            data['img'][h1_tag]=img_tag
    return HttpResponse(json.dumps(data))