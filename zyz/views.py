from django.core.paginator import Paginator # 导入分页模块
from django.shortcuts import render  # 导入渲染模块
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse  # 导入http响应模块
from .models import *  # 导入数据库模型
from django.views import View # 导入视图模块
from django.db.models import Q # 导入查询模块

# Create your views here.


class BaseView(View):
    '''
    检查指定的参数是否存在
    存在返回 True
    不存在返回 False
    '''

    def isExit(param):

        if (param == None) or (param == ''):
            return False
        else:
            return True

    '''
    转换分页查询信息
    '''

    def parasePage(data, count, pageIndex, pageSize, isPage):
        resl = {'data': data, 'count': count, 'pageIndex': pageIndex, 'pageSize': pageSize, 'isPage':isPage}  # 数据 总数  当前页  总页数
        return JsonResponse(resl)


    '''
    成功响应信息
    '''

    def success(msg='处理成功'):
        resl = {'code': 0, 'msg': msg}
        return JsonResponse(resl)

    '''
    成功响应信息, 携带数据
    '''

    def successData(data, msg='处理成功'):
        resl = {'code': 0, 'msg': msg, 'data': data}
        return JsonResponse(resl)

    '''
    系统警告信息
    '''

    def warn(msg='操作异常，请重试'):
        resl = {'code': 1, 'msg': msg}
        return JsonResponse(resl)

    '''
    系统异常信息
    '''

    def error(data,msg='系统异常'):
        resl = {'code': 2, 'msg': msg, 'data': data}
        return JsonResponse(resl)


'''
系统请求处理
'''

class SysView(BaseView):

    def get(self, request, module, *args, **kwargs):
        if module == 'index':  # 首页
            return render(request, 'index.html')
        elif module == 'dashboard':
            return render(request, 'dashboard.html')
        elif module == 'test':
            return render(request, 'test.html')
        elif module == 'user_list':
            return SysView.user_list(request)
        elif module == 'info':  # 用户信息页面
            return SysView.getInfo(request)
        elif module == 'sysnums':  # 系统类容页面
            return SysView.getSysNums(request)
        elif module == 'exit':  # 退出登录
            # 获取session
            del request.session["id"]  # 删除session
            del request.session["role"]  # 删除session

            return HttpResponseRedirect('/jobs/index/')  # 重定向到登录页面
        else:
            return self.error()
    def post(self, request, module, *args, **kwargs):

        if module == 'login':  # 登录

            return SysView.login(request)

        elif module == 'info':  # 更新用户信息
            return SysView.updSessionInfo(request)

        elif module == 'pwd':  # 更新用户密码
            return SysView.updSessionPwd(request)
        elif module == 'register':  # 注册
            return SysView.register(request)
        else:
            return self.error()

    def user_list(request):
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)  #
        name = request.GET.get('query')
        print(name)

        qry = Q()
        if BaseView.isExit(name):
            qry = qry & Q(name__icontains=name)
        print(qry)
        users = User.objects.filter(qry).order_by('create_time')  # 添加 order_by 以对查询结果排序
        paginator = Paginator(users, per_page)  # 分页
        results = []
        for user in paginator.page(page):
            results.append({
                'id': user.id,
                'name': user.name,
                'email': user.email
            })
        return SysView.parasePage(results, users.count(), page, per_page, paginator.num_pages > int(page)) # 数据 总数  当前页  总页数 是否有下一页
    def login(request):
        phone = request.POST.get('phone')  # 获取用户手机号
        password = request.POST.get('password')  # 获取用户密码
        user = User.objects.filter(phone=phone)  # 查询用户是否存在
        # print(user.values())
        if (user.exists()):  # 用户存在
            user = user.first()  # 获取用户对象
            if user.password == password:

                request.session["id"] = user.id  # 将用户id存入session
                request.session["role"] = user.role  # 将用户类型存入session

                return SysView.success()  # 登录成功
            else:
                return SysView.warn('用户密码输入错误')
        else:
            return SysView.warn('用户名输入错误或用户不存在')

    def getInfo(request):
        id = request.session.get('id')
        data = User.objects.filter(id=id)
        # print(data.values())
        datas = {}
        for item in data:
            datas = {
                "name": item.name, # 姓名
                "phone": item.phone, # 手机号
                "email": item.email, # 邮箱
                "password": item.password, # 密码
                "area": item.area, # 地区
                "school": item.school, # 学校
                "major": item.major, # 专业
                "role": item.role, # 用户类型
                "score": item.score, # 积分
                "level": item.level, # 等级
            }

        return SysView.successData(datas)

    def getSysNums(request):

        resl = {
            'sp':Video.objects.filter(status=1).count(),
        }

        return BaseView.successData(resl)

    def updSessionInfo(request):

        user = request.session.get('id')

        User.objects.filter(id=user).update(
            area = request.POST.get('area'),  # 地区
            school = request.POST.get('school'),  # 学校
            major = request.POST.get('major'),  # 专业
            name = request.POST.get('name'),  # 姓名
            email = request.POST.get('email'),  # 邮箱
        )
        return SysView.success()

    def updSessionPwd(request):

        user = request.session.get('id')
        if request.POST.get('password') != '':  # 密码不为空
            print(request.POST.get('password'))
            User.objects.filter(id=user).update(
                password=request.POST.get('password'),
            )

            return SysView.success()
        return SysView.error('密码不能为空')

    def register(request):

        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(phone=phone)
        if user.exists():
            return SysView.warn('用户已存在')
        else:
            User.objects.create(
                phone=phone,
                email=email,
                password=password,
            )
            return SysView.success()


'''
志愿者相关操作
'''

class VolunteersView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            pass
        elif module == 'yu':
            pass

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            pass
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()


'''
活动相关操作
'''

class Activitys(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'showadd':
            return render(request, 'add_activity.html')
        elif module == 'showmgt':
            return render(request, 'mgt_activity.html')
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getPageInfo(request):

        page = request.POST.get('page')
        per_page = request.POST.get('per_page')
        name = request.POST.get('name')
        status = request.POST.get('status')
        qry = Q()
        if name != '':
            qry = qry & Q(name__icontains=name)
        if status != '':
            qry = qry & Q(status=status)
        print(qry)
        activitys = Activity.objects.filter(qry).order_by('create_time')
        total = activitys.count()
        activitys = activitys[(int(page) - 1) * int(per_page):int(page) * int(per_page)]
        resl = {
            'total': total,
            'data': list(activitys.values()),
        }
        return BaseView.successData(resl)

'''
视频相关操作
'''

class Videos(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'showadd':
            return render(request, 'add_video.html')
        elif module == 'showmgt':
            return render(request, 'mgt_video.html')
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()

    def getPageInfo(request):
        pass
'''
问题答复相关
'''


class Problem(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'problem.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()


'''

'''


class GuestsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'projectLogs.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()


'''

'''


class SuperAdminsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'sendLogs.html')
        elif module == 'info':
            return self.getInfo(request)
        elif module == 'page':
            return self.getPageInfo(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        else:
            return self.error()