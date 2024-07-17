from rest_framework import serializers
from .models import User

class UserSignUpRequestSerializer(serializers.Serializer):
    # 이메일
    email = serializers.EmailField(
        help_text="사용할 이메일 주소",
        required=True,
        allow_blank=False,
    )
    # 비밀번호
    password = serializers.CharField(
        max_length=128,
        help_text='사용할 비밀번호 (평문)',
        required=True,
        allow_blank=False,
    )
    # 폰번호
    phone = serializers.CharField(
        max_length=11,
        min_length=11,
        help_text='휴대전화번호(반드시 0~9 사이의 연속된 문자열)',
        required=False,
        allow_blank=True,
    )
    # 이름
    name = serializers.CharField(
        max_length=128,
        help_text='이름',
        required=True,
    )
    # 생년월일
    birthday = serializers.DateField(
        format='%Y-%m-%d',
        input_formats=['%Y-%m-%d', ],
        help_text='생년월일 8자리(나이 계산용)',
        required=True,
    )
    # 성별
    gender = serializers.ChoiceField(
        help_text='성별',
        choices=User.gender_choice,
        required=True
    )

    def get_data_for_user_create(self):
        """
        유저 생성에 필요한 데이터를 반환하는 메서드
        """
        return {
            'email': self.validated_data.get('email'),
            'password': self.validated_data.get('password'),
            'phone': self.validated_data.get('phone'),
            'name': self.validated_data.get('name'),
            'birthday': self.validated_data.get('birthday'),
            'gender': self.validated_data.get('gender'),
        }
