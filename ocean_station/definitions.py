from enum import Enum


class Region(Enum):
    Unset = (0, 'Chose the region', '請選擇地區')
    Northern = (1, 'Northern', '北部')
    Central = (2, 'Central', '中部')
    Southern = (3, 'Southern', '南部')
    Eastern = (4, 'Eastern', '東部')


class ContentFlag(Enum):
    Overview = (1, 'Overview', '概述')
    Title = (2, 'Title', '標題')
    Subtitle = (3, 'Subtitle', '副標題')
    Content = (4, 'Content', '內文')
    Explanation = (5, 'Explanation', '說明')
    TrafficInfo = (6, 'Traffic Information', '交通資訊')
    Cautions = (7, 'Cautions', '注意事項')
    Other = (8, 'Other', '其他')


class PhotoFlag(Enum):
    Main = (1, 'Main', '主要')
    Display = (2, 'Display', '顯示')
    Poster = (3, 'Poster', '海報、標語')
    Activity = (4, 'Activity', '活動')
    Publicity = (5, 'Publicity', '宣傳')
