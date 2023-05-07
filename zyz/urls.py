from django.urls import path
import zyz.views as views

urlpatterns = [
    path('<str:module>/', views.SysView.as_view()),  # 通用接口
    path('volunteers/<str:module>/', views.VolunteersView.as_view()),  # 志愿者相关操作
    path('volunteer_admins/<str:module>/', views.VolunteerAdminsView.as_view()),  # 志愿者管理员相关操作
    path('resource_admins/<str:module>/', views.ResourceAdminsView.as_view()),  # 资源管理员相关操作
    path('answer_admins/<str:module>/', views.AnswerAdminsView.as_view()),  # 答复管理员相关操作
    path('guests/<str:module>/', views.GuestsView.as_view()),  # 游客相关操作
    path('super_admins/<str:module>/', views.SuperAdminsView.as_view()),  # 超级管理员相关操作
]
