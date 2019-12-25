# coding=utf-8


class ImportantLevel:

    LOWER = 1
    NORMAL = 2
    HIGHER = 3

    CHOICES = [
        (LOWER, '低优先级'),
        (NORMAL, '一般'),
        (HIGHER, '高优先级')
    ]


class OrderStatus:

    AUDIT = 0
    CONFIRM = 1
    INBOUNDING = 2
    FINISH = 3
    REFUSED = 4
    EXPIRED = 5
    DELETED = 6

    CHOICES = [
        (AUDIT, '待审核'),
        (CONFIRM, '审核通过'),
        (INBOUNDING, '入库中'),
        (FINISH, '完成'),
        (REFUSED, '审核不通过'),
        (EXPIRED, '已过期'),
        (DELETED, '已删除'),
    ]


class InboundInfoSchema:

    SCHEMA = {
        'title': '出库单信息',
        'type': 'object',
        'options': {'collapsed': True},
        'properties': {
            'task_list': {
                'type': 'array',
                'title': '任务列表',
                'uniqueItems': False,
                'format': 'table',
                'items': {
                    'type': 'object',
                    'title': '任务信息',
                    'properties': {
                        'material': {
                            'type': 'object',
                            'title': '物料信息',
                            'properties': {
                                "material_id": {
                                    'type': 'integer',
                                    'title': '物料ID'
                                },
                                "material_number": {
                                    'type': 'string',
                                    'title': '物料编号'
                                },
                                "material_name": {
                                    'type': 'string',
                                    'title': '物料名'
                                },
                                "material_ser_number": {
                                    "type": "string",
                                    "title": "物料批次"
                                },
                                "count": {
                                    'type': 'integer',
                                    'title': '物料数量'
                                }
                            }
                        },
                        'location': {
                            'type': 'object',
                            'title': '库位信息',
                            'properties': {
                                "location_id": {
                                    'type': 'integer',
                                    'title': '库位ID'
                                },
                                "location_number": {
                                    'type': 'string',
                                    'title': '库位编号'
                                },
                                "action": {
                                    'type': 'integer',
                                    'title': '出入库'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
