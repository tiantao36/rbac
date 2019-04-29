import re
from django.shortcuts import redirect,HttpResponse,render
from django.conf import settings

class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class RbacMiddleware(MiddlewareMixin):
    def process_request(self,request):
        # 1. 当前请求URL
        current_request_url = request.path_info

        # 2. 处理白名单  可以访问登录和admin
        for url in settings.VALID_URL_LIST:
            if re.match(url,current_request_url):
                return None


        # 3. 获取session中保存的权限信息,没有session返回到登录页面
        permission_url = request.session.get(settings.XX)
        if not permission_url:
            return redirect(settings.RBAC_LOGIN_URL)

        # 4. 处理权限匹配不了直接跳转到首页
        flag = False
        for url in permission_url:
            regex = settings.URL_FORMAT.format(url)
            if re.match(regex, current_request_url):
                flag = True
                print('##################')
                break
            if flag:
                break
        if not flag:
            return render(request,'error.html',context={'status':'页面无权访问'})

        def process_exception(self,request,exception):
            return render(request, 'error.html',context={'status':'页面500程序处理错误'})
        def process_response(self, request, response):
            if response.status_code == 404:
                return render(request, 'error.html',context={'status':'页面404不存在'})
            return response