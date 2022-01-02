from enum import Enum

from multi_relation.definitions import Status


class ReservationUsages(Enum):
    OfficialBusiness = (1, 'Official Business', '公務需求')
    Guidance = (2, 'Guidance', '視導需求')
    FamilyVisit = (3, 'Family Visit', '眷探需求')
    Other = (4, 'Other', '其他需求')


class ReservationStatus(Enum):
    Pending = (1, 'Pending', "審查中")
    Passed = (2, 'Passed', "審查通過")
    Failed = (3, 'Failed', "審核失敗")
    Canceled = (4, 'Canceled', '此訂單已取消')
    CheckedIn = (5, 'Check In', "已入住")
    NoShow = (6, 'No Show', '未入住')
    CheckedOut = (7, 'Check Out', '此訂單已退房')


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
