# coding=utf-8


class StoreAreaType:

    BREAD_LINE = 1
    BUCKET_LINE = 2
    VIRTUAL_AREA = 3

    CHOICES = [
        (BREAD_LINE, '面包线'),
        (BUCKET_LINE, '桶装线'),
        (VIRTUAL_AREA, '虚拟区')
    ]


class StoreAreaStatus:

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