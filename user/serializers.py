from rest_framework import serializers
from core.serializers import ResponseBaseSerializer
from .models import User

class UserSignUpRequestSerializer(serializers.Serializer):
    '''
        유저 회원가입 요청 시리얼라이저
    '''
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
            'birthday': self.validated_data.get('birthday').strftime('%Y%m%d'),
            'gender': self.validated_data.get('gender'),
        }


# 유저 로그인 요청 시리얼라이저
class UserSignInRequestSerializer(serializers.Serializer):
    # 유저 이메일
    email = serializers.EmailField()
    # 유저 비밀번호
    password = serializers.CharField()

# 유저 로그인 응답 시리얼라이저
class UserSignInResponseSerializer(ResponseBaseSerializer):
    class UserSignInResponseBody(serializers.Serializer):
        # 액세스 토큰
        def get_access_token(self, instance):
            return self.context.get('access_token')
        # 리프레쉬 토큰
        def get_refresh_token(self, instance):
            return self.context.get('refresh_token')
        # user uuid
        def get_user_uuid(self, instance:User):
            return instance.external_uuid

        access_token = serializers.SerializerMethodField()
        refresh_token = serializers.SerializerMethodField()
        user_uuid = serializers.SerializerMethodField()

    result = UserSignInResponseBody()