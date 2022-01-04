from enum import Enum


class Status(Enum):
    Pending = (1, 'Pending', "審查中")
    Passed = (2, 'Passed', "審查通過")
    Failed = (3, 'Failed', "審核失敗")
    Canceled = (4, 'Canceled', '此訂單已取消')


class PaymentStatus(Enum):
    Unpaid = (1, 'Unpaid', '未付款')
    Paid = (2, 'Paid', '已付款')
    Refund = (3, 'Refunded', '已退款')
