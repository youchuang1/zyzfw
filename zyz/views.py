import json
from datetime import datetime  # 导入时间模块

from django.core.paginator import Paginator  # 导入分页模块
from django.db.models import Q  # 导入查询模块
from django.http import HttpResponseRedirect, JsonResponse  # 导入http响应模块
from django.shortcuts import get_object_or_404  # 导入404模块
from django.shortcuts import render  # 导入渲染模块
from django.utils import timezone  # 导入时间模块
from django.views import View  # 导入视图模块

from .models import *  # 导入数据库模型


# Create your views here.
class DefaultView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/jobs/index/')


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
        resl = {'data': data, 'count': count, 'pageIndex': pageIndex, 'pageSize': pageSize,
                'isPage': isPage}  # 数据 总数  当前页  总页数 是否有下一页
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
    系统异常信息，携带数据
    '''

    def error(data, msg='系统异常'):
        resl = {'code': 2, 'msg': msg, 'data': data}
        return JsonResponse(resl)


'''
系统请求处理
'''


class SysView(BaseView):

    def get(self, request, module, *args, **kwargs):
        if module == 'index':  # 首页
            return render(request, 'index.html')
        elif module == 'login':  # 登录页面
            return render(request, 'login.html')
        elif module == 'dashboard':
            return render(request, 'dashboard.html')
        elif module == 'info':  # 用户信息页面
            return SysView.getInfo(request)
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

    def login(request):
        data = json.loads(request.body)
        phone = data.get('phone')  # 获取用户手机号
        password = data.get('password')  # 获取用户密码
        print(phone, password)
        user = User.objects.filter(phone=phone)  # 查询用户是否存在
        # print(user.values())
        if (user.exists()):  # 用户存在
            user = user.first()  # 获取用户对象
            if user.password == password:

                request.session["id"] = user.id  # 将用户id存入session
                request.session["role"] = user.role  # 将用户类型存入session
                return SysView.success('登录成功')  # 登录成功
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
                "name": item.name,  # 姓名
                "phone": item.phone,  # 手机号
                "email": item.email,  # 邮箱
                "password": item.password,  # 密码
                "area": item.area,  # 地区
                "school": item.school,  # 学校
                "major": item.major,  # 专业
                "role": item.role,  # 用户类型
                "score": item.score,  # 积分
                "level": item.level,  # 等级
            }

        return SysView.successData(datas)

    def updSessionInfo(request):

        user = request.session.get('id')

        User.objects.filter(id=user).update(
            area=request.POST.get('area'),  # 地区
            school=request.POST.get('school'),  # 学校
            major=request.POST.get('major'),  # 专业
            name=request.POST.get('name'),  # 姓名
            email=request.POST.get('email'),  # 邮箱
        )
        return SysView.success('信息修改成功')

    def updSessionPwd(request):
        user = request.session.get('id')
        if request.POST.get('password') != None:  # 密码不为空
            User.objects.filter(id=user).update(
                password=request.POST.get('password'),
            )
            return SysView.success('密码修改成功')
        return SysView.warn('密码不能为空')

    def register(request):
        data = json.loads(request.body)
        phone = data.get('phone')
        email = data.get('email')
        password = data.get('password')

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

    def getPageInfo(self, request):
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)
        query = request.GET.get('query')

        if query:
            users = User.objects.filter(name__icontains=query)
        else:
            users = User.objects.all()

        users = users.order_by('create_time')
        paginator = Paginator(users, per_page)
        page_users = paginator.get_page(page)

        # 我们需要将QuerySet转换为列表，因为JsonResponse不能序列化QuerySet
        user_list = list(page_users.object_list.values())

        # 总用户数
        total_count = paginator.count

        # 判断是否还有下一页
        has_next_page = page_users.has_next()

        return SysView.parasePage(user_list, total_count, page, per_page, has_next_page)

    def addInfo(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        # avatar = request.FILES.get('avatar')  # 获取头像
        if not all([name, phone, ]):
            return SysView.warn('数据不能为空')
        try:
            User.objects.create(
                name=name,
                phone=phone,
                # avatar=avatar,
            )
        except IndexError:
            return SysView.warn('添加失败')
        return SysView.success('添加成功')

    def updInfo(self, request):
        id = request.POST.get('id')
        user = User.objects.get(id=id)

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        # avatar = request.FILES.get('avatar')  # 获取头像

        if name:
            user.name = name
        if phone:
            user.phone = phone
        # if avatar:
        #     user.avatar = avatar

        user.save()
        return SysView.success('更新成功')

    def delInfo(self, request):
        id = request.POST.get('id')
        User.objects.filter(id=id).delete()
        return SysView.success('删除成功')


'''
活动相关操作
'''


class Activitys(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'showadd':
            return render(request, 'add_activity.html')
        elif module == 'showmgt':
            return render(request, 'mgt_activity.html')
        elif module == 'mysignup':
            return render(request, 'mysignup.html')
        elif module == 'eventhall':
            return render(request, 'eventhall.html')
        elif module == 'page':
            return self.getPageInfo(request)
        elif module == 'get':
            return self.gets(request)
        # 活动报名
        elif module == 'apply':
            return self.apply(request)
        # 活动报名列表(审核)
        elif module == 'applylist':
            return self.applyList(request)
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

    def addInfo(self, request):
        title = request.POST.get('title')
        sponsor = request.POST.get('sponsor')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        start_time = timezone.make_aware(datetime.fromisoformat(start_time))
        end_time = timezone.make_aware(datetime.fromisoformat(end_time))
        place = request.POST.get('place')  # 地点
        introduction = request.POST.get('introduction')
        tag = request.POST.get('tag')  # 标签
        score = int(request.POST.get('score'))  # 积分
        apply_num = int(request.POST.get('apply_num'))
        img_path = request.FILES.get('logo')  # 获取图片
        if not all([title, sponsor, start_time, end_time, place, introduction, tag, score, apply_num, img_path]):
            return SysView.error('数据不能为空')
        try:
            Activity.objects.create(
                title=title,
                sponsor=sponsor,
                start_time=start_time,
                end_time=end_time,
                place=place,
                introduction=introduction,
                tag=tag,
                score=score,
                apply_num=apply_num,
                img_path=img_path,
                status=1,
                applied_num=0,
            )
        except IndexError:
            return SysView.error('添加失败')
        return SysView.success('添加成功')

    def getPageInfo(self, request):
        page = request.GET.get('page', 1)  # 当前页
        per_page = request.GET.get('per_page', 10)  # 每页显示条数
        name = request.GET.get('name', '')  # 活动名称
        status = request.GET.get('status', '')  # 活动状态

        qry = Q()
        if name:
            qry = qry & Q(title__icontains=name)
        if status:
            qry = qry & Q(status=status)

        activities = Activity.objects.filter(qry).order_by('start_time')  # 添加 order_by 以对查询结果排序
        paginator = Paginator(activities, per_page)  # 分页
        results = []
        for activity in paginator.page(page):
            results.append({
                'id': activity.id,  # 活动id
                'title': activity.title,  # 活动名称
                'sponsor': activity.sponsor,  # 主办方
                'start_time': activity.start_time,  # 开始时间
                'end_time': activity.end_time,  # 结束时间
                'place': activity.place,  # 活动地点
                'introduction': activity.introduction,  # 活动简介
                'tag': activity.tag,  # 活动标签
                'score': activity.score,  # 活动积分
                'apply_num': activity.apply_num,  # 活动人数
                'applied_num': activity.applied_num,  # 已报名人数
                'status': activity.status,  # 活动状态
                'img_path': activity.img_path.url if activity.img_path else None,  # 活动图片
                'create_time': activity.create_time,  # 创建时间
            })

        return BaseView.parasePage(results, activities.count(), page, per_page,
                                   paginator.num_pages > int(page))  # 数据、总数、当前页、总页数、是否有下一页

    def updInfo(self, request):
        id = request.POST.get('id')
        activity = get_object_or_404(Activity, id=id)  # 获取活动

        title = request.POST.get('title')
        sponsor = request.POST.get('sponsor')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        if start_time and end_time:
            start_time = timezone.make_aware(datetime.fromisoformat(start_time))
            end_time = timezone.make_aware(datetime.fromisoformat(end_time))
        place = request.POST.get('place')
        introduction = request.POST.get('introduction')
        tag = request.POST.get('tag')
        score = request.POST.get('score')
        if score:
            score = int(score)
        apply_num = request.POST.get('apply_num')
        if apply_num:
            apply_num = int(apply_num)
        img_path = request.FILES.get('logo')  # 获取图片

        if title:
            activity.title = title
        if sponsor:
            activity.sponsor = sponsor
        if start_time:
            activity.start_time = start_time
        if end_time:
            activity.end_time = end_time
        if place:
            activity.place = place
        if introduction:
            activity.introduction = introduction
        if tag:
            activity.tag = tag
        if score is not None:
            activity.score = score
        if apply_num is not None:
            activity.apply_num = apply_num
        if img_path:
            activity.img_path = img_path

        activity.save()
        return SysView.success('更新成功')

    def delInfo(self, request):
        id = request.POST.get('id')
        Activity.objects.filter(id=id).delete()
        return SysView.success('删除成功')

    def apply(self, request):
        id = request.POST.get('id')
        user_id = request.POST.get('user_id')  # assuming you have user_id in the request
        activity = get_object_or_404(Activity, id=id)  # use get_object_or_404 instead

        if activity.applied_num >= activity.apply_num:
            return SysView.error('报名人数已满')

        # create a new Activity_apply object
        Activity_apply.objects.create(
            activity=activity,
            user_id=user_id,
            status=0  # assuming 0 is for pending review
        )

        activity.applied_num += 1
        activity.save()

        return SysView.success('报名成功')

    def applyList(self, request):
        id = request.GET.get('id')
        activity = get_object_or_404(Activity, id=id)
        applications = Activity_apply.objects.filter(activity=activity)
        results = [{'user_id': application.user_id, 'status': application.status, 'apply_time': application.create_time}
                   for application in applications]  # 用户id、状态、报名时间
        return SysView.successData(results, '获取成功')

    def gets(self, request):
        id = request.GET.get('id')
        activity = get_object_or_404(Activity, id=id)
        results = {
            'id': activity.id,  # 活动id
            'title': activity.title,  # 活动名称
            'sponsor': activity.sponsor,  # 主办方
            'start_time': activity.start_time,  # 开始时间
            'end_time': activity.end_time,  # 结束时间
            'place': activity.place,  # 活动地点
            'introduction': activity.introduction,  # 活动简介
            'tag': activity.tag,  # 活动标签
            'score': activity.score,  # 活动积分
            'apply_num': activity.apply_num,  # 活动人数
            'status': activity.status,  # 活动状态
            'img_path': activity.img_path.url if activity.img_path else None,  # 活动图片
        }
        return SysView.successData(results, '获取成功')


'''
视频相关操作
'''


class Videos(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'showadd':
            return render(request, 'add_video.html')
        elif module == 'showmgt':
            return render(request, 'mgt_video.html')
        elif module == 'mystudies':
            return render(request, 'mystudies.html')
        elif module == 'videohall':
            return render(request, 'videohall.html')
        elif module == 'page':
            return self.getPageInfo(request)
        elif module == 'get':
            return self.gets(request)
        else:
            return self.error()

    def post(self, request, module, *args, **kwargs):
        if module == 'add':
            return self.addInfo(request)
        elif module == 'del':
            return self.delInfo(request)
        elif module == 'upd':
            return self.updInfo(request)
        else:
            return self.error()

    def getPageInfo(self, request):
        page = request.GET.get('page', 1)  # 当前页
        per_page = request.GET.get('per_page', 10)  # 每页显示条数
        name = request.GET.get('name', '')  # 视频名称
        type = request.GET.get('type', '')  # 视频类型

        qry = Q()
        if name:
            qry = qry & Q(title__icontains=name)
        if type:
            qry = qry & Q(type=type)

        videos = Video.objects.filter(qry).order_by('create_time')  # 添加 order_by 以对查询结果排序
        paginator = Paginator(videos, per_page)  # 分页
        results = []
        for video in paginator.page(page):
            results.append({
                'id': video.id,  # 视频id
                'title': video.title,  # 视频名称
                'introduction': video.introduction,  # 视频简介
                'tag': video.tag,  # 视频类型
                'score': video.score,  # 视频积分
                'img_path': video.img_path.url if video.img_path else None,  # 视频封面
                'video_path': video.video_path.url if video.video_path else None,  # 视频路径
                'create_time': video.create_time,  # 创建时间
            })
        return BaseView.parasePage(results, videos.count(), page, per_page,
                                   paginator.num_pages > int(page))  # 数据、总数、当前页、总页数、是否有下一页

    def addInfo(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        tags = request.POST.get('tags')
        cover_image = request.FILES.get('cover_image')
        points = request.POST.get('points')
        video_file = request.FILES.get('video_file')
        type = request.POST.get('type')

        if not all([title, description, tags, cover_image, points, video_file, type]):
            return SysView.warn('数据不能为空')
        try:
            Video.objects.create(
                title=title,
                introduction=description,
                tag=tags,
                img_path=cover_image,
                score=points,
                video_path=video_file,
                type=type
            )
        except IndexError:
            return SysView.warn('添加失败')
        return SysView.success('上传成功')

    def delInfo(self, request):
        id = request.POST.get('id')
        Video.objects.filter(id=id).delete()
        return SysView.success('删除成功')

    def updInfo(self, request):
        id = request.POST.get('id')
        video = get_object_or_404(Video, id=id)

        title = request.POST.get('title')
        description = request.POST.get('description')
        tags = request.POST.get('tags')
        cover_image = request.FILES.get('cover_image')
        points = request.POST.get('points')
        if points:
            points = int(points)
        video_file = request.FILES.get('video_file')
        type = request.POST.get('type')

        if title:
            video.title = title
        if description:
            video.description = description
        if tags:
            video.tags = tags
        if cover_image:
            video.cover_image = cover_image
        if points is not None:
            video.points = points
        if video_file:
            video.video_file = video_file
        if type:
            video.type = type

        video.save()
        return SysView.success('更新成功')

    def gets(self, request):
        id = request.GET.get('id')
        video = get_object_or_404(Video, id=id)
        results = {
            'id': video.id,  # 视频id
            'title': video.title,  # 视频名称
            'introduction': video.introduction,  # 视频简介
            'tag': video.tag,  # 视频类型
            'score': video.score,  # 视频积分
            'img_path': video.img_path.url if video.img_path else None,  # 视频封面
            'video_path': video.video_path.url if video.video_path else None,  # 视频路径
            'create_time': video.create_time,  # 创建时间
        }
        return SysView.successData(results, '获取成功')


'''
问题答复相关
'''

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

    def getPageInfo(self, request):
        page = request.GET.get('page', 1)  # 获取当前页，默认为1
        per_page = request.GET.get('per_page', 10)  # 每页显示的问题数，默认为10
        query = request.GET.get('query')  # 查询参数，比如问题的标题

        qry = Q()
        if query:
            qry = qry & Q(title__icontains=query)

        # 获取问题及其相关的回答
        prefetch = Prefetch('answer_set', queryset=Answer.objects.all())
        questions = Question.objects.filter(qry).prefetch_related(prefetch).order_by('create_time')

        # 对问题进行分页
        paginator = Paginator(questions, per_page)
        page_questions = paginator.get_page(page)

        # 将问题及其相关回答转换为可以序列化的格式
        question_list = []
        for question in page_questions:
            answers = [{'content': answer.content, 'user_id': answer.user_id, 'create_time': answer.create_time}
                       for answer in question.answer_set.all()]
            question_list.append({
                'id': question.id,
                'title': question.title,
                'content': question.content,
                'user_id': question.user_id,
                'status': question.status,
                'create_time': question.create_time,
                'answers': answers
            })

        # 总问题数
        total_count = paginator.count

        # 判断是否还有下一页
        has_next_page = page_questions.has_next()

        # 使用 BaseView 的 parsePage 方法返回分页信息
        return BaseView.parasePage(question_list, total_count, page, per_page, has_next_page)  # 数据、总数、当前页、总页数、是否有下一页

    def addInfo(self, request):
        title = request.POST.get('title')
        content = request.POST.get('content')
        user_id = request.POST.get('user_id')

        if not all([title, content, user_id]):
            return BaseView.warn('数据不能为空')

        try:
            question = Question.objects.create(title=title, content=content, user_id=user_id, status=0)
            return BaseView.successData({'id': question.id})
        except Exception as e:
            return BaseView.warn('添加失败')

    def updInfo(self, request):
        question_id = request.POST.get('id')
        title = request.POST.get('title')
        content = request.POST.get('content')

        try:
            question = Question.objects.get(id=question_id)
        except ObjectDoesNotExist:
            return BaseView.warn('修改失败')

        if title:
            question.title = title
        if content:
            question.content = content

        question.save()
        return BaseView.success('修改成功')

    def delInfo(self, request):
        question_id = request.POST.get('id')

        try:
            question = Question.objects.get(id=question_id)
            question.delete()
            return BaseView.success('删除成功')
        except ObjectDoesNotExist:
            return BaseView.warn('问题不存在')

'''


class GuestsView(BaseView):

    def get(self, request, module, *args, **kwargs):

        if module == 'show':
            return render(request, 'guests.html')
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

    def getInfo(self, request):
        pass

    def getPageInfo(self, request):
        pass

    def addInfo(self, request):
        pass

    def updInfo(self, request):
        pass

    def delInfo(self, request):
        pass


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

'''
