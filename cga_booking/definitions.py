from enum import Enum


class Usages(Enum):
    OfficialBusiness = (1, 'Official Business', '公務需求')
    Guidance = (2, 'Guidance', '視導需求')
    FamilyVisit = (3, 'Family Visit', '眷探需求')
    Other = (4, 'Other', '其他需求')


class ReservationStatus(Enum):
    HalfDone = (1, 'Half Done', "訂單已送出，住宿人員未完成")
    Pending = (2, 'Pending', "此訂單待審查")
    Passed = (3, 'Passed', "審查通過")
    CheckedIn = (4, 'Check In', "已入住")
    NoShow = (5, 'No Show', '未入住')
    CheckedOut = (6, 'Check Out', '此訂單已退房')
    Canceled = (7, 'Canceled', '此訂單已取消')


class PaymentStatus(Enum):
    Unpaid = (1, 'Unpaid', '未付款')
    Paid = (2, 'Paid', '已付款')


class Gender(Enum):
    Female = (0, 'Female', '女性')
    Male = (1, 'Male', '男性')
    Privacy = (2, 'Privacy', '不公開')


class ContentFlag(Enum):
    Overview = (1, 'Overview', '概述')
    Title = (2, 'Title', '標題')
    Content = (3, 'Content', '內文')
    Cautions = (4, 'Cautions', '注意事項')
    Other = (5, 'Other', '其他')
