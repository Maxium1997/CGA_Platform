from enum import Enum


class Gender(Enum):
    Unset = (0, 'Unset', '未設定')
    Male = (1, 'Male', '男性')
    Female = (2, 'Female', '女性')
    Privacy = (3, 'Privacy', '不公開')


class Identity(Enum):
    Unset = (0, 'Unset', '未設定')
    Citizen = (1, 'Citizen', '公民')
    CivilServant = (2, 'Civil Servant', '公務員')
    Military = (3, 'Military', '軍職')
    Police = (4, 'Police', '警職')


class Privilege(Enum):
    Superuser = (0b11111111, 'Super User', '超級使用者')
    User = (0b1, 'User', '使用者')


class CivilServant(Enum):
    pass


class MilitaryRank(Enum):
    pass


class PoliceRank(Enum):
    pass
