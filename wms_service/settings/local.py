from wms_service.settings.base import *

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "wms_service",
        "HOST": "192.168.3.246",
        "PORT": 3306,
        "USER": 'root',
        "PASSWORD": "new.123",
        "OPTIONS": {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
