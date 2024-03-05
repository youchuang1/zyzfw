from django.db import models

# Create your models here.


"""
用户表
"""
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12,verbose_name='姓名')
    phone = models.CharField(max_length=11,verbose_name='手机号')
    email = models.CharField(max_length=20,verbose_name='邮箱')
    password = models.CharField(max_length=30,verbose_name='密码')
    area = models.CharField(max_length=40,verbose_name='地区')
    school = models.CharField(max_length=40,verbose_name='学校')
    major = models.CharField(max_length=20,verbose_name='专业')
    role = models.IntegerField(default=0,verbose_name='角色') # 0:普通用户 1:志愿者 2:管理员
    score = models.IntegerField(default=0,verbose_name='积分')
    level = models.IntegerField(default=0,verbose_name='等级')
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

"""
活动表  0:未开始 1:进行中 2:已结束
"""
class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20,verbose_name='标题')
    sponsor = models.CharField(max_length=20,verbose_name='主办方')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    place = models.CharField(max_length=40,verbose_name='地点')
    introduction = models.CharField(max_length=100,verbose_name='简介')
    tag = models.CharField(max_length=20,verbose_name='标签')
    score = models.IntegerField(verbose_name='积分')
    apply_num = models.IntegerField(verbose_name='允许申请人数')
    applied_num = models.IntegerField(verbose_name='已申请人数')
    status = models.IntegerField(verbose_name='状态') # 0:未开始 1:进行中 2:已结束
    img_path = models.ImageField(upload_to='file/img',verbose_name='活动logo图片路径')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table = 'activity'
        verbose_name = '活动'
        verbose_name_plural = verbose_name

"""
活动申请表
"""
class Activity_apply(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activity,on_delete=models.CASCADE,verbose_name='活动id')
    user_id = models.IntegerField(verbose_name='用户id')
    status = models.IntegerField(verbose_name='状态') # 0:未审核 1:已通过 2:未通过
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table = 'activity_apply'
        verbose_name = '活动申请'
        verbose_name_plural = verbose_name

"""
视频表
"""
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20,verbose_name='标题')
    introduction = models.CharField(max_length=100,verbose_name='简介')
    tag = models.CharField(max_length=20,verbose_name='标签')
    img_path = models.ImageField(upload_to='file/img',verbose_name='视频封面图片路径')
    score = models.IntegerField(verbose_name='积分')
    video_path = models.FileField(upload_to='file/video',verbose_name='视频路径')
    # 视频类型
    type = models.IntegerField(verbose_name='类型') # 0:医学课程 1:养育课程 2:教育课程
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table = 'video'
        verbose_name = '视频'
        verbose_name_plural = verbose_name

"""
视频学习表
"""
class Video_study(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.ForeignKey(Video,on_delete=models.CASCADE,verbose_name='视频id')
    user_id = models.IntegerField(verbose_name='用户id')
    status = models.IntegerField(verbose_name='状态') # 0:未学习 1:已学习
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table = 'video_study'
        verbose_name = '视频学习'
        verbose_name_plural = verbose_name

"""
提问表
"""
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20,verbose_name='标题')
    content = models.CharField(max_length=100,verbose_name='内容')
    user_id = models.IntegerField(verbose_name='用户id')
    status = models.IntegerField(verbose_name='状态') # 0:未回复 1:已回复
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table = 'question'
        verbose_name = '提问'
        verbose_name_plural = verbose_name

"""
回答表
"""
class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question,on_delete=models.CASCADE,verbose_name='问题id')
    content = models.CharField(max_length=100,verbose_name='内容')
    user_id = models.IntegerField(verbose_name='用户id')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table = 'answer'
        verbose_name = '回答'
        verbose_name_plural = verbose_name