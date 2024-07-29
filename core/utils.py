import enum


# Enum 클래스에 대해서 Choice 튜플을 반환하는 메서드를 추가한 클래스
class EnumChoice(enum.Enum):
    @classmethod
    def get_choice(cls):
        return tuple(
            (value_obj.name, value_obj.value) for value_obj in cls.__members__.values()
        )

def calculate_pagination_max_page(total_items, items_per_page):
    """
    # number pagination에서
    # max_page 구하는 유틸
    """
    import math
    if items_per_page == 0:
        return 0  # 페이지당 항목 수가 0이면 0 페이지로 반환
    return math.ceil(total_items / items_per_page)