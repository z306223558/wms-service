from wms_service.settings.base import *
from wms_service.settings.template_settings.simple_ui import *
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
