# coding=utf-8


class StoreLocationType:

    RANDOM_LOCATION = 1
    PRODUCT_LOCATION = 2

    CHOICES = [
        (RANDOM_LOCATION, '随机库位'),
        (PRODUCT_LOCATION, '生成库位')
    ]


class StoreLocationWarningType:

    NORMAL = 0
    USE_RATE_LOW = 1
    EXPIRE_WARN = 2
    MIX_COUNT_HIGH = 3

    CHOICES = [
        (NORMAL, '无'),
        (USE_RATE_LOW, '利用率低'),
        (EXPIRE_WARN, '过期接近')
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