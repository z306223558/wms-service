# coding=utf-8
import time

# 显示服务器信息
SIMPLEUI_HOME_INFO = False

# 关闭simplepro的版本信息
SIMPLEPRO_INFO = False

SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menu_display': ['用户管理', '仓库管理', '入库管理', '出库管理', '报表管理', '盘点管理', '系统设置'],
    # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
    'dynamic': True,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus': [{
        'name': '用户管理',
        'icon': 'fas fa-user-shield',
        'models': [{
            'name': '用户',
            'icon': 'fa fa-user',
            'url': '/wms/user/user/'
        }, {
            'name': '个人信息',
            'icon': 'fa fa-user',
            'url': '/wms/user/profile/'
        }, {
            'name': '权限管理',
            'icon': 'fa fa-group',
            'url': '/wms/auth/group/'
        }]
    }, {
        'name': '仓库管理',
        'icon': 'fa fa-warehouse',
        'models': [{
            'name': '库区管理',
            'icon': 'fa fa-warehouse',
            'url': '/wms/area/storearea/'
        }, {
            'name': '库位管理',
            'icon': 'fa fa-braille',
            'url': '/wms/location/storelocation/'
        }, {
            'name': '物料管理',
            'icon': 'fa fa-cube',
            'url': '/wms/material/material/'
        }, {
            'name': '物料分类',
            'icon': 'fa fa-cubes',
            'url': '/wms/material/materialcategory/'
        }, {
            'name': '分类添加物料',
            'icon': 'fa fa-plus-square',
            'url': '/wms/material/materialcategoryrecord/'
        }, {
            'name': '物料入库记录',
            'icon': 'fa fa-table',
            'url': '/wms/material/materiallocationrecord/'
        }]
    }, {
        'name': '入库管理',
        'icon': 'fa fa-desktop',
        'models': [{
            'name': '入库管理',
            'url': 'http://baidu.com',
            'icon': 'far fa-surprise'
        }]
    }, {
        'name': '出库管理',
        'icon': 'fa fa-desktop',
        'models': [{
            'name': '出库管理',
            'url': 'http://baidu.com',
            'icon': 'far fa-surprise'
        }]
    }, {
        'name': '报表管理',
        'icon': 'fa fa-desktop',
        'models': [{
            'name': '报表管理',
            'url': 'http://baidu.com',
            'icon': 'far fa-surprise'
        }]
    }, {
        'name': '盘点管理',
        'icon': 'fa fa-desktop',
        'models': [{
            'name': '盘点管理',
            'url': 'http://baidu.com',
            'icon': 'far fa-surprise'
        }]
    }, {
        'name': '系统设置',
        'icon': 'fa fa-desktop',
        'models': [{
            'name': '系统设置',
            'url': 'http://baidu.com',
            'icon': 'far fa-surprise'
        }]
    }]
}
