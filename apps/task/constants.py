# coding=utf-8


class TaskStatus:

    CONFIRM = 0
    RUNNING = 1
    FINISH = 3
    ERROR = 4
    EXPIRED = 5
    DELETED = 6

    CHOICES = [
        (CONFIRM, '待开始'),
        (RUNNING, '正在进行'),
        (ERROR, '任务错误'),
        (FINISH, '完成'),
        (EXPIRED, '已过期'),
        (DELETED, '已删除'),
    ]


class TaskType:

    INBOUND = 1
    OUTBOUND = 2
    MOVE = 3
    CHECK = 4
    REPORT = 5

    CHOICES = [
        (INBOUND, '入库任务'),
        (OUTBOUND, '出库任务'),
        (MOVE, '移库任务'),
        (CHECK, '盘点任务'),
        (REPORT, '报表任务')
    ]

    ORDER_PREFIX = ['IN', 'OT', 'MV', 'CK', 'RP']


class TaskActions:

    IN = 1
    OUT = 2
    CHECK = 3

    CHOICES = [
        (IN, '放入'),
        (OUT, '取出'),
        (CHECK, '盘点')
    ]
