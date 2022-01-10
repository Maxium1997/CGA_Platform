from enum import Enum


class TopicStatus(Enum):
    Published = (1, 'Published', '公開')  # show for anyone
    Privacy = (2, 'Privacy', '不公開')     # show for some specific people
    Stored = (3, 'Stored', '典藏')    # show for myself
    Special = (4, 'Special Collection', '精選')
    # The following status are been reported will be use.
    Reported = (5, 'Reported', '被檢舉')
    Pending = (6, 'Pending', '待審核')
    Passed = (7, 'Passed', '審核通過')
