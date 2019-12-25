# coding=utf-8

import os
import sys
import datetime
from typing import Any, Callable, Union
import djcelery
from django.contrib.admin import AdminSite

location: Callable[[Any], Union[bytes, str]] = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), x)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
sys.path.insert(0, os.path.join(BASE_DIR, './apps'))
sys.path.insert(0, os.path.join(BASE_DIR, './extra_apps'))

SECRET_KEY = '7@!37shu)x%2ivfv26kkecjsm#$hb5$o(yq9r-44v@%-s)c@ue'
DEBUG = True

# IP访问控制
ALLOWED_HOSTS = ['*', ]
INTERNAL_IPS = ALLOWED_HOSTS

# 功能模板加载
DEFAULT_APPS = [
    # 'jet.dashboard',
    # 'jet',
    'simplepro',
    'simpleui',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]
OTHER_APPS = [
    'corsheaders',
    # 'djcelery',
    # 'kombu.transport.django',
    'easy_select2',
    'drf_yasg',
    'rest_framework',
    'django_filters',
    'debug_toolbar',
    'django_mysql',
]
PROJECT_APPS = [
    'user.apps.UserConfig',
    'area.apps.StoreAreaConfig',
    'inbound.apps.InboundConfig',
    'location.apps.StoreLocationConfig',
    'material.apps.MaterialConfig',
    # 'inbound.apps.InboundConfig',
    'outbound.apps.OutboundConfig',
    'schedule.apps.ScheduleConfig',
    'stocktaking.apps.StocktakingConfig',
    'task.apps.TaskConfig',
]
INSTALLED_APPS = OTHER_APPS + DEFAULT_APPS + PROJECT_APPS
SITE_ID = 1

# 中间件配置
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# 跨域请求配置
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '*'
)
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# 基本路由配置
ROOT_URLCONF = 'wms_service.urls'

# 模板数据配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'wms_service.wsgi.application'

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "wms_service",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": 'root',
        "PASSWORD": "new.123",
        "OPTIONS": {
            'charset': 'utf8mb4'
        },
    }
}

# 缓存配置：目前使用redis缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": "",
        },
    }
}
REST_FRAMEWORK_EXTENSIONS = {
    # 过期时间  单位是秒
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60 * 24
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# 密码验证设置
AUTH_USER_MODEL = "user.User"
AUTHENTICATION_BACKENDS = (
    'apps.user.auth_backend.MobileAuthBackend',
    'apps.user.auth_backend.UsernameAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6
        }
    }]

# 日志系统配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },  # 针对 DEBUG = True 的情况
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(filename)s %(module)s %(funcName)s %(lineno)d: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True  # 是否继承父类的log信息
        },  # handlers 来自于上面的 handlers 定义的内容
    }
}

# 基本系统配置
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False
DEFAULT_CHARSET = "UTF-8"
DEFAULT_DECIMAL_PLACES = 2
DEFAULT_MAX_DIGITS = 12
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000

# REST支持
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DATETIME_FORMAT': DATETIME_FORMAT,
    'DATETIME_INPUT_FORMATS': [DATETIME_FORMAT],
    'DATE_FORMAT': DATE_FORMAT,
    'DATE_INPUT_FORMATS': [DATE_FORMAT]
}

# 是否支持前端改写cookie
SESSION_COOKIE_HTTPONLY = False

# 静态资源配置
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'wms_service', 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'wms_service', 'media')
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 上传大小配置50M
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'

# 接口文档swagger配置
SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'none',
    'DEFAULT_MODEL_DEPTH': -1,
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'LOGIN_URL': '/admin/login/',
    'LOGOUT_URL': '/admin/logout/',
}

# JWT登录支持，用来做权限验证
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'Token',
    # 'JWT_ALLOW_REFRESH': True,
    # 'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

# 后台系统JET配置
JET_THEMES = [
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]
JET_SIDE_MENU_COMPACT = True
JET_INDEX_DASHBOARD = 'dashboards.DefaultIndexDashboard'
JET_APP_INDEX_DASHBOARD = 'dashboards.DefaultIndexDashboard'
JET_SIDE_MENU_CUSTOM_APPS = [
    ('user', ['__all__'])
]

# # 配置celery任务队列
# CELERY_ACCEPT_CONTENT = ['application/json', ]
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
#
# CELERY_IMPORTS = (
#     'plantform.tasks'
# )
#
# # celery时区设置，使用settings中TIME_ZONE同样的时区
# djcelery.setup_loader()
# BROKER_URL = 'django://'
