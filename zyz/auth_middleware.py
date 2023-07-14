from django.shortcuts import redirect
from django.http import HttpResponseRedirect


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        index_url = '/jobs/index/'  # 首页的 URL
        login_url = '/jobs/login/'  # 登录页面的 URL
        is_login_page = request.path.startswith(login_url)  # 请求的页面是否为登录页面
        is_static_file = request.path.startswith('/static/')  # 请求的页面是否为静态文件

        # 将不需要验证的页面添加到此列表中
        excluded_urls = [
            '/jobs/index/',
            '/jobs/register/',
        ]
        is_excluded = any(request.path.startswith(url) for url in excluded_urls)

        if not is_excluded and not is_login_page and not is_static_file and not request.session.get('id'):
            # 如果用户未登录且请求的页面需要验证，将其重定向到登录页面
            return HttpResponseRedirect(index_url)

        # 如果用户已登录或请求的页面不需要验证，调用 self.get_response(request) 并返回响应
        response = self.get_response(request)
        return response