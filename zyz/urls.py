from django.urls import path
import zyz.views as views

urlpatterns = [
    path('<str:module>/', views.SysView.as_view()),  # 通用接口
    path('volunteers/<str:module>/', views.VolunteersView.as_view()),  # 志愿者相关操作
    path('activity/<str:module>/', views.Activitys.as_view()),  # 活动相关操作
    path('video/<str:module>/', views.Videos.as_view()),  # 视频相关操作
    path('problem/<str:module>/', views.Problem.as_view()),  # 问题相关操作
    path('guests/<str:module>/', views.GuestsView.as_view()),  # 志愿者管理相关操作
    path('super_admins/<str:module>/', views.SuperAdminsView.as_view()),  #
]
