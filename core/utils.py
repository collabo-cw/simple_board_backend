import enum


# Enum 클래스에 대해서 Choice 튜플을 반환하는 메서드를 추가한 클래스
class EnumChoice(enum.Enum):
    @classmethod
    def get_choice(cls):
        return tuple(
            (value_obj.name, value_obj.value) for value_obj in cls.__members__.values()
        )