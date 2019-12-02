# coding=utf-8


class MaterialQuality:

    SEMI_PRODUCT = 4
    REJECT_PRODUCT = 5
    GOOD_PRODUCT = 1
    INSPECTION_PRODUCT = 3

    CHOICES = [
        (SEMI_PRODUCT, '半成品'),
        (REJECT_PRODUCT, '不良品'),
        (GOOD_PRODUCT, '良品'),
        (INSPECTION_PRODUCT, '待检品')
    ]


class OperateSource:

    PC_WEBSITE = 1
    MOBILE_WEBSITE = 2
    WEBAPP = 3
    WEIXIN_WEBSITE = 4
    IOS_APP = 5
    ANDROID_APP = 6
    PDR = 7
    WEIXIN_MINI_APP = 8

    CHOICES = [
        (PC_WEBSITE, '电脑端网页'),
        (MOBILE_WEBSITE, '移动端M站'),
        (WEBAPP, 'WebAPP'),
        (WEIXIN_WEBSITE, '微信网页'),
        (IOS_APP, 'IOS客户端'),
        (ANDROID_APP, 'Android客户端'),
        (PDR, '工厂PDR设备'),
        (WEIXIN_MINI_APP, '微信小程序')
    ]


class MaterialStatus:

    INSPECTION = 3
    WAIT_ENTRY = 0
    NORMAL = 1
    IN_ENTRY = 2
    EXPIRED = 4
    DELETE = -1
    IN_OUT = 5
    OUTED = 6
    PACKING = 7

    CHOICES = [
        (INSPECTION, '待检'),
        (WAIT_ENTRY, '待入库'),
        (NORMAL, '在库'),
        (IN_ENTRY, '正在入库'),
        (EXPIRED, '已过期'),
        (DELETE, '删除'),
        (IN_OUT, '在出库'),
        (OUTED, '已出库'),
        (PACKING, '正在打包')
    ]


