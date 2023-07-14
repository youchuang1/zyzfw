"""
Django settings for zyzfw project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-r^n$^%clohl^*##s*wu%m9%x1f7yj@fhab20)+2ib2oh_5o7pb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']  # 允许访问的主机名，如果是*，则允许所有主机访问

# Application definition

""" 应用 """
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'zyz'
]

""" 中间件 """""
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 安全中间件
    'django.contrib.sessions.middleware.SessionMiddleware',  # 会话中间件
    'django.middleware.common.CommonMiddleware',  # 通用中间件
    # 'django.middleware.csrf.CsrfViewMiddleware', # 跨站请求伪造中间件
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 认证中间件
    'django.contrib.messages.middleware.MessageMiddleware',  # 消息中间件
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 点击劫持中间件
    'zyz.auth_middleware.AuthMiddleware',  # 自定义认证中间件
]

ROOT_URLCONF = 'zyzfw.urls'  # 根路由

""" 模板 """
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # 模板引擎
        'DIRS': []  # 模板目录
        ,
        'APP_DIRS': True,  # 是否使用应用程序目录
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # 调试模式
                'django.template.context_processors.request',  # 请求上下文
                'django.contrib.auth.context_processors.auth',  # 认证上下文
                'django.contrib.messages.context_processors.messages',  # 消息上下文
            ],
        },
    },
]

WSGI_APPLICATION = 'zyzfw.wsgi.application'  # WSGI应用程序

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

""" 默认数据库 """""
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

""" mysql数据库 """
DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'zyzfw',
            'HOST': '127.0.0.1',
            'PORT': 3306,
            'USER': 'root',
            'PASSWORD': '123456',
        }
}
# cookies过期时间
# SESSION_COOKIE_AGE = 60 * 60 * 24 * 1 # 1天

# session过期时间
SESSION_EXPIRE_AT_BROWSER_CLOSE = 60 * 60 * 24 * 1  # 1天

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

""" 密码验证 """
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # 用户属性相似性验证器
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # 最小长度验证器
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # 常用密码验证器
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # 数字密码验证器
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # 语言代码

TIME_ZONE = 'Asia/Shanghai'  # 时区

USE_I18N = True  # 使用国际化

USE_TZ = True  # 使用时区

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'  # 静态文件URL

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'file')  # 媒体文件根目录
MEDIA_URL = '/file/'  # 媒体文件URL
