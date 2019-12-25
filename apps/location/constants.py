# coding=utf-8


class StoreLocationType:
    RANDOM_LOCATION = 1
    PRODUCT_LOCATION = 2

    CHOICES = [
        (RANDOM_LOCATION, '随机库位'),
        (PRODUCT_LOCATION, '生产库位')
    ]


class StoreLocationWarningType:
    NORMAL = 0
    USE_RATE_LOW = 1
    EXPIRE_WARN = 2
    MIX_COUNT_HIGH = 3

    CHOICES = [
        (NORMAL, '无'),
        (USE_RATE_LOW, '利用率低'),
        (EXPIRE_WARN, '过期接近'),
        (MIX_COUNT_HIGH, '种类过多')
    ]


class StoreLocationStatus:
    NORMAL = 1
    FORBIDDEN = 0
    DELETED = -1
    REPAIR = 2

    CHOICES = [
        (NORMAL, '正常'),
        (FORBIDDEN, '停用'),
        (DELETED, '已删除'),
        (REPAIR, '检修中'),
    ]


class StoreLocationMaterialsSchema:

    SCHEMA = {
        'title': '在库物料信息',
        'type': 'object',
        'options': {'collapsed': True},
        'properties': {
            'materials': {
                'type': 'array',
                'title': '物料列表',
                'uniqueItems': False,
                'format': 'table',
                'items': {
                    'type': 'object',
                    'title': '物料',
                    'properties': {
                        'name': {
                            'type': 'string',
                            'title': '物料名称'
                        },
                        'id': {
                            'type': 'integer',
                            'title': '物料ID'
                        },
                        'count': {
                            'type': 'integer',
                            'title': '在库库存数量'
                        },
                        'expired_date': {
                            'type': 'string',
                            'format': 'datetime',
                            'title': '过期时间'
                        },
                        'inbound_date': {
                            'type': 'string',
                            'format': 'datetime',
                            'title': '入库时间'
                        }
                    }
                }
            }
        }
    }
