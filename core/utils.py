import enum
import os
from functools import wraps
from django.db import transaction
from rest_framework import serializers

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

def validate_file_extension(value):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.avi', '.mov']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise serializers.ValidationError("허용되는 파일 형식은 이미지와 동영상 파일만 가능합니다.")
    return value

# 연속적인 DB 작업의 경우
# 특정정보는 생성되고 특정정보는 생성되지 않으면 안된다.
# 하나의 뷰에서 일어나는 모든 DB 입출력은 원자성을 가져야함
# 때문에 try-except로 캐치할 수 있는 에러에 대해서는
# 완전한 원자성을 보장하는 데코레이터가 필요하다.
# 강력한 트랜잭션 적용
def set_atomic_transaction(func):
    @wraps(func)
    @transaction.atomic()
    def decorator(*args, **kwargs):
        from django.db import transaction
        initial_savepoint = transaction.savepoint()
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print('에러가 발생하여 DB작업 초기화 : ', e)
            transaction.savepoint_rollback(initial_savepoint)
            from core.models import APIResponseHandler
            return APIResponseHandler.CODE_0008.get_status_response()

    return decorator