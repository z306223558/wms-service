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
